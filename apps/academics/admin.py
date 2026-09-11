from django.contrib import admin
from .models import SchoolClass, Section, Subject, ClassRoutine


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'branch', 'order', 'is_active')
    list_filter = ('is_active', 'branch')
    search_fields = ('name', 'code')
    ordering = ('order',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'school_class', 'capacity', 'is_active')
    list_filter = ('is_active', 'school_class')
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'school_class', 'full_marks', 'pass_marks', 'is_active')
    list_filter = ('is_active', 'school_class')
    search_fields = ('name', 'code')


@admin.register(ClassRoutine)
class ClassRoutineAdmin(admin.ModelAdmin):
    list_display = ('section', 'subject', 'day', 'start_time', 'end_time')
    list_filter = ('day', 'section')
    search_fields = ('section__name', 'subject__name')