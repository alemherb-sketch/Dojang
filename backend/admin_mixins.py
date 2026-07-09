"""Shared admin mixins for the Dojang admin.

RowActionsMixin appends an "Acciones" column with Editar / Eliminar icon
buttons to every changelist it is mixed into. Styling lives in
templates/admin/base_site.html (classes prefixed ``djd-row-action``) so it
does not depend on Unfold's precompiled Tailwind subset.
"""
from django.contrib import admin
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class RowActionsMixin:
    """Adds a trailing column of Editar/Eliminar icon links to the changelist.

    Mix in *before* the concrete ModelAdmin base so ``get_list_display``
    cooperatively calls through to it, e.g.::

        class GradeAdmin(RowActionsMixin, ModelAdmin):
            ...
    """
    
    change_form_show_cancel_button = True

    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        if "acciones" not in list_display:
            list_display.append("acciones")
        return list_display

    def has_change_permission(self, request, obj=None):
        if request.GET.get("view") == "1":
            return False
        return super().has_change_permission(request, obj)

    @admin.display(description=_("Acciones"))
    def acciones(self, obj):
        meta = obj._meta
        parts = []

        try:
            change_url = reverse(
                f"admin:{meta.app_label}_{meta.model_name}_change", args=[obj.pk]
            )
            parts.append(
                format_html(
                    '<a href="{}?view=1" class="djd-row-action djd-row-action--view" '
                    'title="{}"><span class="material-symbols-outlined">visibility</span></a>',
                    change_url,
                    _("Ver"),
                )
            )
            parts.append(
                format_html(
                    '<a href="{}" class="djd-row-action djd-row-action--edit" '
                    'title="{}"><span class="material-symbols-outlined">edit</span></a>',
                    change_url,
                    _("Editar"),
                )
            )
        except NoReverseMatch:
            pass

        try:
            delete_url = reverse(
                f"admin:{meta.app_label}_{meta.model_name}_delete", args=[obj.pk]
            )
            parts.append(
                format_html(
                    '<a href="{}" class="djd-row-action djd-row-action--delete" '
                    'title="{}"><span class="material-symbols-outlined">delete</span></a>',
                    delete_url,
                    _("Eliminar"),
                )
            )
        except NoReverseMatch:
            pass

        if not parts:
            return "—"

        return format_html(
            '<div class="djd-row-actions">{}</div>', mark_safe("".join(parts))
        )
