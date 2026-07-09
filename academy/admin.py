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

@admin.register(Activity)
class ActivityAdmin(RowActionsMixin, ModelAdmin):
    list_display = ('title', 'date_posted', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
