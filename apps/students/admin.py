from django.contrib import admin
from .models import Student, Guardian


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'relation', 'phone', 'email', 'occupation')
    search_fields = ('full_name', 'phone', 'email')
    list_filter = ('relation',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'gender', 'branch', 'group', 'roll_no', 'admission_date', 'is_active')
    list_filter = ('is_active', 'gender', 'branch', 'group')
    search_fields = ('student_id', 'full_name', 'phone', 'email')
    filter_horizontal = ('guardians',)
    readonly_fields = ('created_at', 'updated_at')