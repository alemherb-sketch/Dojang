from django.contrib import admin
from unfold.admin import ModelAdmin
from backend.admin_mixins import RowActionsMixin
from .models import Grade, Section, Activity

@admin.register(Grade)
class GradeAdmin(RowActionsMixin, ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)

@admin.register(Section)
class SectionAdmin(RowActionsMixin, ModelAdmin):
    list_display = ('name', 'schedule', 'instructor')
    search_fields = ('name',)
    list_filter = ('instructor',)
    filter_horizontal = ('students',)

from django.utils.html import format_html

@admin.register(Activity)
class ActivityAdmin(RowActionsMixin, ModelAdmin):
    list_display = ('title', 'date_posted', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
    fields = ('title', 'content', 'image', 'image_preview', 'is_active')
    readonly_fields = ('image_preview',)

    class Media:
        js = ('js/image_preview.js',)

    @admin.display(description='Vista previa de imagen')
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height: 250px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);" />', obj.image.url)
        return "No hay imagen cargada"
