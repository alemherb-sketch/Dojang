from django import forms
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.decorators import action

from backend.admin_mixins import RowActionsMixin
from .credentials import build_username, generate_password
from .models import Parent, Student, User, generate_qr_token
from .qr import qr_svg


def _student_card(student):
    return {
        'name': student.get_full_name().strip() or student.username,
        'username': student.username,
        'svg': mark_safe(qr_svg(student.qr_code, module_px=6)) if student.qr_code else '',
    }


class CustomUserAdmin(RowActionsMixin, BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Información Adicional', {'fields': ('role', 'phone_number', 'parent')}),
        ('Código QR', {'fields': ('qr_code', 'qr_preview')}),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined'), 'classes': ('collapse',)}),
    )
    readonly_fields = ('qr_preview',)
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    actions = ('print_qr_cards',)

    @admin.display(description=_('Vista previa del QR'))
    def qr_preview(self, obj):
        if not obj or not obj.qr_code:
            return mark_safe(
                '<span style="color:#94a3b8">Se generará automáticamente al guardar '
                '(solo alumnos).</span>'
            )
        return format_html(
            '<div style="display:inline-block;padding:.6rem;background:#fff;'
            'border:1px solid #e2e8f0;border-radius:.6rem">{}</div>'
            '<div style="margin-top:.4rem;font-family:monospace;font-size:.8rem;'
            'color:#64748b">{}</div>',
            mark_safe(qr_svg(obj.qr_code, module_px=5)),
            obj.qr_code,
        )

    @admin.action(description=_('Imprimir carnets QR'))
    def print_qr_cards(self, request, queryset):
        cards = []
        for user in queryset:
            if user.role == 'STUDENT' and not user.qr_code:
                user.qr_code = generate_qr_token()
                user.save(update_fields=['qr_code'])
            if not user.qr_code:
                continue
            cards.append(_student_card(user))
        return render(request, 'admin/users/qr_cards.html', {'cards': cards})


admin.site.register(User, CustomUserAdmin)


# Remove the built-in Group model entirely to avoid confusion with Student Groups
admin.site.unregister(Group)


class CredentialAdmin(RowActionsMixin, ModelAdmin):
    """Base admin for proxy roles whose portal credentials are auto-issued.

    On creation the username (from DNI or name) and a random password are
    generated automatically — the admin never types them — and revealed once.
    """
    role_value = None
    username_fallback = 'usuario'
    credential_role_label = 'usuario'

    def save_model(self, request, obj, form, change):
        if obj.role != self.role_value:
            obj.role = self.role_value
        if not change:
            if not obj.username:
                obj.username = build_username(
                    dni=obj.dni,
                    first_name=obj.first_name,
                    last_name=obj.last_name,
                    fallback=self.username_fallback,
                )
            
            raw_password = form.cleaned_data.get('password') if hasattr(form, 'cleaned_data') else None
            if not raw_password:
                raw_password = generate_password()
                obj._generated_password = raw_password
            obj.set_password(raw_password)
            obj.portal_password = raw_password
        super().save_model(request, obj, form, change)

    def _credentials_context(self, obj):
        raw = getattr(obj, '_generated_password', None)
        if not raw:
            return None
        return {
            'username': obj.username,
            'password': raw,
            'role_label': self.credential_role_label,
        }

    actions_detail = ('reset_password_detail',)

    @admin.action(description=_('Restablecer contraseña del portal'))
    def reset_password(self, request, queryset):
        for user in queryset:
            raw = generate_password()
            user.set_password(raw)
            user.portal_password = raw
            user.save(update_fields=['password', 'portal_password'])
            messages.success(
                request,
                f'{user.get_full_name().strip() or user.username} — '
                f'nueva contraseña: {raw}',
            )

    @action(description=_('Generar Nueva Contraseña'))
    def reset_password_detail(self, request, object_id):
        user = self.get_object(request, object_id)
        if user:
            raw = generate_password()
            user.set_password(raw)
            user.portal_password = raw
            user.save(update_fields=['password', 'portal_password'])
            messages.success(
                request,
                f'Nueva contraseña generada para {user.username}: {raw} (anótala ahora, por seguridad no se volverá a mostrar)',
            )
        return redirect(request.META.get('HTTP_REFERER', '.'))


class ParentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True), required=False, label="Contraseña", help_text="Déjelo en blanco para auto-generar.")

    class Meta:
        model = Parent
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'dni', 'phone_number', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].required = False


@admin.register(Parent)
class ParentAdmin(CredentialAdmin):
    role_value = 'PARENT'
    username_fallback = 'apoderado'
    credential_role_label = 'apoderado'
    form = ParentForm
    actions = ('reset_password',)
    list_display = ('username', 'first_name', 'last_name', 'dni', 'phone_number')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'dni', 'phone_number')

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return (
                ('Credenciales de Acceso', {
                    'fields': ('username', 'password'),
                    'description': 'Puede escribir las credenciales o dejar los campos en blanco para que el sistema las genere automáticamente.',
                }),
                ('Información Personal', {
                    'fields': ('first_name', 'last_name', 'email', 'dni', 'phone_number', 'address'),
                }),
            )
        return (
            ('Acceso al portal', {'fields': ('username', 'portal_password')}),
            ('Información Personal', {
                'fields': ('first_name', 'last_name', 'email', 'dni', 'phone_number', 'address'),
            }),
        )

    def get_readonly_fields(self, request, obj=None):
        return ('username', 'portal_password') if obj else ()

    def response_add(self, request, obj, post_url_continue=None):
        creds = self._credentials_context(obj)
        if creds:
            messages.success(
                request,
                f'Apoderado creado. Credenciales del portal — Usuario: {creds["username"]}  |  '
                f'Contraseña: {creds["password"]}  (anótala, no se volverá a mostrar).',
            )
        return super().response_add(request, obj, post_url_continue)


class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True), required=False, label="Contraseña", help_text="Déjelo en blanco para auto-generar.")

    class Meta:
        model = Student
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'dni', 'birth_date',
                  'address', 'blood_type', 'phone_number', 'parent')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].required = False


@admin.register(Student)
class StudentAdmin(CredentialAdmin):
    role_value = 'STUDENT'
    username_fallback = 'alumno'
    credential_role_label = 'alumno / apoderado'
    form = StudentForm
    actions = ('print_qr_cards', 'reset_password')
    list_display = ('username', 'first_name', 'last_name', 'dni', 'phone_number')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'dni')

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return (
                ('Credenciales de Acceso', {
                    'fields': ('username', 'password'),
                    'description': 'Puede escribir las credenciales o dejar los campos en blanco para que el sistema las genere automáticamente.',
                }),
                ('Información Personal', {
                    'fields': ('first_name', 'last_name', 'email', 'dni', 'birth_date',
                               'address', 'blood_type', 'phone_number', 'parent'),
                }),
            )
        return (
            ('Acceso al portal', {'fields': ('username', 'portal_password')}),
            ('Información Personal', {
                'fields': ('first_name', 'last_name', 'email', 'dni', 'birth_date',
                           'address', 'blood_type'),
            }),
            ('Datos del Alumno', {'fields': ('phone_number', 'parent')}),
            ('Carnet QR', {'fields': ('qr_code', 'qr_preview', 'carnet_link')}),
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('username', 'portal_password', 'qr_code', 'qr_preview', 'carnet_link')
        return ()

    @admin.display(description=_('Vista previa del QR'))
    def qr_preview(self, obj):
        if not obj or not obj.qr_code:
            return mark_safe('<span style="color:#94a3b8">Se generará al guardar.</span>')
        return format_html(
            '<div style="display:inline-block;padding:.6rem;background:#fff;'
            'border:1px solid #e2e8f0;border-radius:.6rem">{}</div>'
            '<div style="margin-top:.4rem;font-family:monospace;font-size:.8rem;'
            'color:#64748b">{}</div>',
            mark_safe(qr_svg(obj.qr_code, module_px=5)),
            obj.qr_code,
        )

    @admin.display(description=_('Carnet'))
    def carnet_link(self, obj):
        if not obj or not obj.pk:
            return '—'
        url = reverse('admin:users_student_carnet', args=[obj.pk])
        return format_html(
            '<a href="{}" target="_blank" class="djd-row-action djd-row-action--edit" '
            'style="width:auto;padding:0 .9rem;gap:.4rem">'
            '<span class="material-symbols-outlined">badge</span> Imprimir carnet</a>',
            url,
        )

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                '<int:pk>/carnet/',
                self.admin_site.admin_view(self.carnet_view),
                name='users_student_carnet',
            ),
        ]
        return custom + urls

    def carnet_view(self, request, pk):
        student = self.get_object(request, pk)
        if student is None:
            raise Http404('Alumno no encontrado')
        if not student.qr_code:
            student.qr_code = generate_qr_token()
            student.save(update_fields=['qr_code'])
        context = {
            'cards': [_student_card(student)],
            'back_url': reverse('admin:users_student_changelist'),
        }
        return render(request, 'admin/users/qr_cards.html', context)

    @admin.action(description=_('Imprimir carnets QR'))
    def print_qr_cards(self, request, queryset):
        cards = []
        for student in queryset:
            if not student.qr_code:
                student.qr_code = generate_qr_token()
                student.save(update_fields=['qr_code'])
            cards.append(_student_card(student))
        return render(request, 'admin/users/qr_cards.html', {'cards': cards})

    def response_add(self, request, obj, post_url_continue=None):
        if '_addanother' not in request.POST and '_continue' not in request.POST:
            context = {
                'cards': [_student_card(obj)],
                'credentials': self._credentials_context(obj),
                'back_url': reverse('admin:users_student_changelist'),
            }
            return render(request, 'admin/users/qr_cards.html', context)
        creds = self._credentials_context(obj)
        if creds:
            messages.success(
                request,
                f'Alumno creado. Usuario: {creds["username"]}  |  '
                f'Contraseña: {creds["password"]}  (anótala, no se volverá a mostrar).',
            )
        return super().response_add(request, obj, post_url_continue)
