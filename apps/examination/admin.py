from django.contrib import admin
from .models import Exam, ExamSchedule, ExamResult, AdmitCard


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_type', 'school_class', 'start_date', 'end_date', 'is_active')
    list_filter = ('exam_type', 'is_active', 'school_class')
    search_fields = ('name',)


@admin.register(ExamSchedule)
class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = ('exam', 'subject', 'date', 'start_time', 'end_time', 'room')
    list_filter = ('exam', 'date')
    search_fields = ('exam__name', 'subject__name')


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'subject', 'marks_obtained', 'grade', 'is_absent')
    list_filter = ('exam', 'grade', 'is_absent')
    search_fields = ('student__full_name', 'student__student_id')


@admin.register(AdmitCard)
class AdmitCardAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'roll_no', 'is_issued', 'issued_at')
    list_filter = ('is_issued', 'exam')
    search_fields = ('student__full_name', 'roll_no')