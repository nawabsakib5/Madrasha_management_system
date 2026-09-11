from django.contrib import admin
from .models import Staff, LeaveType, LeaveApplication


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'full_name', 'staff_type', 'gender', 'branch', 'designation', 'joining_date', 'is_active')
    list_filter = ('is_active', 'staff_type', 'gender', 'branch')
    search_fields = ('staff_id', 'full_name', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_days', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ('staff', 'leave_type', 'start_date', 'end_date', 'status', 'approved_by')
    list_filter = ('status', 'leave_type')
    search_fields = ('staff__full_name',)