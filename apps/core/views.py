from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AuditLog, LoginAttempt


@login_required
def dashboard_view(request):
    user = request.user
    context = {
        'user': user,
        'role': user.role,
    }

    if user.role in ['platform_superuser', 'super_admin', 'admin']:
        try:
            from apps.students.models import Student
            from apps.staff.models import Staff
            from apps.accounting.models import FeePayment
            from apps.attendance.models import StudentAttendance
            import datetime
            today = datetime.date.today()
            context.update({
                'total_students': Student.objects.filter(is_active=True).count(),
                'total_staff': Staff.objects.filter(is_active=True).count(),
                'today_attendance': StudentAttendance.objects.filter(date=today).count(),
                'recent_payments': FeePayment.objects.filter(is_void=False).order_by('-paid_at')[:5],
            })
        except Exception:
            pass

    elif user.role == 'teacher':
        try:
            from apps.attendance.models import StudentAttendance
            import datetime
            today = datetime.date.today()
            context.update({
                'today_attendance': StudentAttendance.objects.filter(date=today).count(),
            })
        except Exception:
            pass

    elif user.role == 'student':
        try:
            from apps.students.models import Student
            from apps.accounting.models import FeeInvoice
            student = Student.objects.get(user=user)
            context.update({
                'student': student,
                'pending_fees': FeeInvoice.objects.filter(
                    student=student,
                    status='unpaid'
                ).count(),
            })
        except Exception:
            pass

    elif user.role == 'parent':
        try:
            from apps.students.models import Student
            context.update({
                'children': Student.objects.filter(guardians__user=user),
            })
        except Exception:
            pass

    return render(request, 'core/dashboard.html', context)


@login_required
def audit_log_view(request):
    logs = AuditLog.objects.all().order_by('-timestamp')[:100]
    return render(request, 'core/audit_log.html', {'logs': logs})