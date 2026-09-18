from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Exam, ExamSchedule, ExamResult, AdmitCard
from apps.academics.models import SchoolClass, Subject
from apps.students.models import Student


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


# ─── Exam ─────────────────────────────────────────────────
@role_required('platform_superuser', 'super_admin', 'admin', 'teacher')
def exam_list(request):
    exams = Exam.objects.all().order_by('-start_date')
    return render(request, 'examination/exam_list.html', {'exams': exams})


@role_required('platform_superuser', 'super_admin', 'admin')
def exam_add(request):
    if request.method == 'POST':
        try:
            exam = Exam(
                name=request.POST.get('name'),
                exam_type=request.POST.get('exam_type'),
                school_class=SchoolClass.objects.get(pk=request.POST.get('school_class')),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
            )
            exam.save()
            messages.success(request, f'Exam {exam.name} সফলভাবে তৈরি হয়েছে।')
            return redirect('examination:exam_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    classes = SchoolClass.objects.filter(is_active=True)
    return render(request, 'examination/exam_form.html', {
        'action': 'Add',
        'classes': classes,
        'exam_type_choices': Exam.EXAM_TYPE_CHOICES,
    })


# ─── Exam Result ──────────────────────────────────────────
@role_required('platform_superuser', 'super_admin', 'admin', 'teacher')
def result_list(request):
    results = ExamResult.objects.all().order_by('-exam__start_date')
    return render(request, 'examination/result_list.html', {'results': results})


@role_required('platform_superuser', 'super_admin', 'admin', 'teacher')
def result_add(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)
    students = Student.objects.filter(is_active=True)
    subjects = Subject.objects.filter(school_class=exam.school_class)

    if request.method == 'POST':
        try:
            student = Student.objects.get(pk=request.POST.get('student'))
            subject = Subject.objects.get(pk=request.POST.get('subject'))
            marks = request.POST.get('marks_obtained')
            is_absent = request.POST.get('is_absent') == 'on'

            # Auto grade calculation
            marks_float = float(marks) if marks else 0
            if is_absent:
                grade = 'F'
            elif marks_float >= 80:
                grade = 'A+'
            elif marks_float >= 70:
                grade = 'A'
            elif marks_float >= 60:
                grade = 'A-'
            elif marks_float >= 50:
                grade = 'B'
            elif marks_float >= 40:
                grade = 'C'
            elif marks_float >= 33:
                grade = 'D'
            else:
                grade = 'F'

            result, created = ExamResult.objects.get_or_create(
                exam=exam,
                student=student,
                subject=subject,
                defaults={
                    'marks_obtained': marks_float,
                    'grade': grade,
                    'is_absent': is_absent,
                }
            )
            if not created:
                result.marks_obtained = marks_float
                result.grade = grade
                result.is_absent = is_absent
                result.save()

            messages.success(request, 'Result সফলভাবে সংরক্ষণ হয়েছে।')
            return redirect('examination:result_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'examination/result_form.html', {
        'exam': exam,
        'students': students,
        'subjects': subjects,
    })


# ─── Admit Card ───────────────────────────────────────────
@role_required('platform_superuser', 'super_admin', 'admin')
def admit_card_list(request):
    admit_cards = AdmitCard.objects.all().order_by('-exam__start_date')
    return render(request, 'examination/admit_card_list.html', {'admit_cards': admit_cards})


@role_required('platform_superuser', 'super_admin', 'admin')
def admit_card_generate(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)
    students = Student.objects.filter(is_active=True)

    if request.method == 'POST':
        try:
            generated = 0
            for i, student in enumerate(students, 1):
                roll_no = f'{exam.pk}{str(i).zfill(3)}'
                admit_card, created = AdmitCard.objects.get_or_create(
                    exam=exam,
                    student=student,
                    defaults={'roll_no': roll_no}
                )
                generated += 1

            messages.success(request, f'{generated} জন student-এর admit card তৈরি হয়েছে।')
            return redirect('examination:admit_card_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'examination/admit_card_generate.html', {
        'exam': exam,
        'students': students,
    })