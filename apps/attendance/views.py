from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import StudentAttendance, StaffAttendance
from apps.students.models import Student
from apps.staff.models import Staff
import datetime


def role_required(*roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.role not in roles:
                messages.error(request, 'আপনার এই page দেখার permission নেই।')
                return redirect('core:dashboard')
            return view_func(request, *args, **kwargs)
        wrapper.__wrapped__ = view_func
        return login_required(wrapper)
    return decorator


# ─── Student Attendance ───────────────────────────────────
# Student-দের attendance হাজিরা খাতা থেকে manual input

@role_required('platform_superuser', 'super_admin', 'admin', 'teacher')
def student_attendance_list(request):
    date = request.GET.get('date', str(datetime.date.today()))
    attendances = StudentAttendance.objects.filter(date=date).order_by('student__student_id')
    return render(request, 'attendance/student_attendance_list.html', {
        'attendances': attendances,
        'date': date,
    })


@role_required('platform_superuser', 'super_admin', 'admin', 'teacher')
def student_attendance_mark(request):
    # হাজিরা খাতা থেকে manual input
    today = datetime.date.today()
    students = Student.objects.filter(is_active=True)

    if request.method == 'POST':
        try:
            date = request.POST.get('date', str(today))
            for student in students:
                status = request.POST.get(f'status_{student.pk}', 'absent')
                note = request.POST.get(f'note_{student.pk}', '')

                attendance, created = StudentAttendance.objects.get_or_create(
                    student=student,
                    date=date,
                    defaults={'status': status, 'note': note}
                )
                if not created:
                    attendance.status = status
                    attendance.note = note
                    attendance.save()

            messages.success(request, f'{date} তারিখের হাজিরা সফলভাবে সংরক্ষণ হয়েছে।')
            return redirect('attendance:student_attendance_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    existing = {a.student_id: a for a in StudentAttendance.objects.filter(date=today)}

    return render(request, 'attendance/student_attendance_mark.html', {
        'students': students,
        'today': today,
        'existing': existing,
        'status_choices': StudentAttendance.STATUS_CHOICES,
    })


# ─── Staff Attendance ─────────────────────────────────────
# Staff/Teacher attendance দুইভাবে আসবে:
# 1. Access Control device থেকে auto import
# 2. Manual input

@role_required('platform_superuser', 'super_admin', 'admin')
def staff_attendance_list(request):
    date = request.GET.get('date', str(datetime.date.today()))
    attendances = StaffAttendance.objects.filter(date=date).order_by('staff__staff_id')
    return render(request, 'attendance/staff_attendance_list.html', {
        'attendances': attendances,
        'date': date,
    })


@role_required('platform_superuser', 'super_admin', 'admin')
def staff_attendance_mark(request):
    # Manual input
    today = datetime.date.today()
    staffs = Staff.objects.filter(is_active=True)

    if request.method == 'POST':
        try:
            date = request.POST.get('date', str(today))
            source = request.POST.get('source', 'manual')  # manual বা access_control

            for staff in staffs:
                status = request.POST.get(f'status_{staff.pk}', 'absent')
                check_in = request.POST.get(f'check_in_{staff.pk}', '')
                check_out = request.POST.get(f'check_out_{staff.pk}', '')
                note = request.POST.get(f'note_{staff.pk}', '')

                attendance, created = StaffAttendance.objects.get_or_create(
                    staff=staff,
                    date=date,
                    defaults={
                        'status': status,
                        'check_in': check_in or None,
                        'check_out': check_out or None,
                        'note': note,
                    }
                )
                if not created:
                    attendance.status = status
                    attendance.check_in = check_in or None
                    attendance.check_out = check_out or None
                    attendance.note = note
                    attendance.save()

            messages.success(request, f'{date} তারিখের staff attendance ({source}) সফলভাবে সংরক্ষণ হয়েছে।')
            return redirect('attendance:staff_attendance_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    existing = {a.staff_id: a for a in StaffAttendance.objects.filter(date=today)}

    return render(request, 'attendance/staff_attendance_mark.html', {
        'staffs': staffs,
        'today': today,
        'existing': existing,
        'status_choices': StaffAttendance.STATUS_CHOICES,
    })


@role_required('platform_superuser', 'super_admin', 'admin')
def staff_attendance_import(request):
    # Access Control device থেকে data import
    # Future: device API থেকে auto sync
    if request.method == 'POST':
        try:
            date = request.POST.get('date', str(datetime.date.today()))
            imported = 0

            # CSV file থেকে import (Access Control export)
            if request.FILES.get('attendance_file'):
                import csv
                import io
                file = request.FILES['attendance_file']
                decoded = file.read().decode('utf-8')
                reader = csv.DictReader(io.StringIO(decoded))

                for row in reader:
                    try:
                        staff = Staff.objects.get(staff_id=row.get('staff_id'))
                        attendance, created = StaffAttendance.objects.get_or_create(
                            staff=staff,
                            date=date,
                            defaults={
                                'status': row.get('status', 'present'),
                                'check_in': row.get('check_in') or None,
                                'check_out': row.get('check_out') or None,
                                'note': 'Access Control Import',
                            }
                        )
                        imported += 1
                    except Staff.DoesNotExist:
                        continue

            messages.success(request, f'{imported} জন staff-এর attendance import হয়েছে।')
            return redirect('attendance:staff_attendance_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'attendance/staff_attendance_import.html')