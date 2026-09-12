from django.contrib import admin
from .models import StudentAttendance, StaffAttendance


@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'section', 'date', 'status', 'note')
    list_filter = ('status', 'date', 'section')
    search_fields = ('student__full_name', 'student__student_id')
    ordering = ('-date',)


@admin.register(StaffAttendance)
class StaffAttendanceAdmin(admin.ModelAdmin):
    list_display = ('staff', 'date', 'status', 'check_in', 'check_out', 'note')
    list_filter = ('status', 'date')
    search_fields = ('staff__full_name', 'staff__staff_id')
    ordering = ('-date',)