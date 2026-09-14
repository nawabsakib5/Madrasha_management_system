from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, Guardian


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


@role_required('platform_superuser', 'super_admin', 'admin')
def student_list(request):
    students = Student.objects.filter(is_active=True).order_by('student_id')
    return render(request, 'students/student_list.html', {'students': students})


@role_required('platform_superuser', 'super_admin', 'admin')
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})


@role_required('platform_superuser', 'super_admin', 'admin')
def student_add(request):
    if request.method == 'POST':
        try:
            student = Student(
                student_id=request.POST.get('student_id'),
                full_name=request.POST.get('full_name'),
                gender=request.POST.get('gender'),
                date_of_birth=request.POST.get('date_of_birth'),
                phone=request.POST.get('phone', ''),
                email=request.POST.get('email', ''),
                address=request.POST.get('address', ''),
                roll_no=request.POST.get('roll_no', ''),
                admission_date=request.POST.get('admission_date'),
            )
            if request.FILES.get('photo'):
                student.photo = request.FILES['photo']
            student.save()
            messages.success(request, f'Student {student.full_name} সফলভাবে যোগ করা হয়েছে।')
            return redirect('students:student_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'students/student_form.html', {'action': 'Add'})


@role_required('platform_superuser', 'super_admin', 'admin')
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        try:
            student.full_name = request.POST.get('full_name')
            student.gender = request.POST.get('gender')
            student.date_of_birth = request.POST.get('date_of_birth')
            student.phone = request.POST.get('phone', '')
            student.email = request.POST.get('email', '')
            student.address = request.POST.get('address', '')
            student.roll_no = request.POST.get('roll_no', '')
            if request.FILES.get('photo'):
                student.photo = request.FILES['photo']
            student.save()
            messages.success(request, f'Student {student.full_name} সফলভাবে আপডেট হয়েছে।')
            return redirect('students:student_detail', pk=student.pk)
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'students/student_form.html', {'action': 'Edit', 'student': student})


@role_required('platform_superuser', 'super_admin', 'admin')
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.is_active = False
        student.save()
        messages.success(request, f'Student {student.full_name} নিষ্ক্রিয় করা হয়েছে।')
        return redirect('students:student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})