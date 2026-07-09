from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    RangeDateFilter,
    RelatedDropdownFilter,
)

from backend.admin_mixins import RowActionsMixin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(RowActionsMixin, ModelAdmin):
    list_display = ('alumno', 'grupo', 'fecha', 'hora_ingreso', 'status_badge')
    list_select_related = ('student', 'section')
    list_filter = (
        ('date', RangeDateFilter),
        ('status', ChoicesDropdownFilter),
        ('section', RelatedDropdownFilter),
    )
    list_filter_submit = True
    date_hierarchy = 'date'
    search_fields = (
        'student__username',
        'student__first_name',
        'student__last_name',
        'student__email',
        'section__name',
    )
    autocomplete_fields = ('student', 'section')
    list_per_page = 50

    @admin.display(description=_('Alumno'), ordering='student__first_name')
    def alumno(self, obj):
        return obj.student.get_full_name().strip() or obj.student.username

    @admin.display(description=_('Grupo'), ordering='section__name')
    def grupo(self, obj):
        return obj.section.name if obj.section else '—'

    @admin.display(description=_('Fecha'), ordering='date')
    def fecha(self, obj):
        return obj.date.strftime('%d/%m/%Y')

    @admin.display(description=_('Hora de ingreso'), ordering='time')
    def hora_ingreso(self, obj):
        return obj.time.strftime('%H:%M')

    @admin.display(description=_('Estado'), ordering='status')
    def status_badge(self, obj):
        colors = {
            'PRESENT': ('#166534', '#dcfce7'),
            'LATE': ('#92400e', '#fef3c7'),
            'ABSENT': ('#991b1b', '#fee2e2'),
        }
        fg, bg = colors.get(obj.status, ('#334155', '#e2e8f0'))
        return format_html(
            '<span style="display:inline-block;padding:.15rem .6rem;border-radius:999px;'
            'font-size:.75rem;font-weight:700;color:{};background:{}">{}</span>',
            fg, bg, obj.get_status_display(),
        )
