from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Staff, LeaveType, LeaveApplication


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
def staff_list(request):
    staffs = Staff.objects.filter(is_active=True).order_by('staff_id')
    return render(request, 'staff/staff_list.html', {'staffs': staffs})


@role_required('platform_superuser', 'super_admin', 'admin')
def staff_detail(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    return render(request, 'staff/staff_detail.html', {'staff': staff})


@role_required('platform_superuser', 'super_admin', 'admin')
def staff_add(request):
    if request.method == 'POST':
        try:
            staff = Staff(
                staff_id=request.POST.get('staff_id'),
                full_name=request.POST.get('full_name'),
                staff_type=request.POST.get('staff_type'),
                gender=request.POST.get('gender'),
                phone=request.POST.get('phone'),
                email=request.POST.get('email', ''),
                address=request.POST.get('address', ''),
                designation=request.POST.get('designation', ''),
                joining_date=request.POST.get('joining_date'),
            )
            if request.FILES.get('photo'):
                staff.photo = request.FILES['photo']
            staff.save()
            messages.success(request, f'Staff {staff.full_name} সফলভাবে যোগ করা হয়েছে।')
            return redirect('staff:staff_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'staff/staff_form.html', {
        'action': 'Add',
        'staff_type_choices': Staff.STAFF_TYPE_CHOICES,
        'gender_choices': Staff.GENDER_CHOICES,
        'blood_group_choices': Staff.BLOOD_GROUP_CHOICES,
    })


@role_required('platform_superuser', 'super_admin', 'admin')
def staff_edit(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        try:
            staff.full_name = request.POST.get('full_name')
            staff.staff_type = request.POST.get('staff_type')
            staff.gender = request.POST.get('gender')
            staff.phone = request.POST.get('phone')
            staff.email = request.POST.get('email', '')
            staff.address = request.POST.get('address', '')
            staff.designation = request.POST.get('designation', '')
            if request.FILES.get('photo'):
                staff.photo = request.FILES['photo']
            staff.save()
            messages.success(request, f'Staff {staff.full_name} সফলভাবে আপডেট হয়েছে।')
            return redirect('staff:staff_detail', pk=staff.pk)
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'staff/staff_form.html', {
        'action': 'Edit',
        'staff': staff,
        'staff_type_choices': Staff.STAFF_TYPE_CHOICES,
        'gender_choices': Staff.GENDER_CHOICES,
        'blood_group_choices': Staff.BLOOD_GROUP_CHOICES,
    })


@role_required('platform_superuser', 'super_admin', 'admin')
def staff_delete(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff.is_active = False
        staff.save()
        messages.success(request, f'Staff {staff.full_name} নিষ্ক্রিয় করা হয়েছে।')
        return redirect('staff:staff_list')
    return render(request, 'staff/staff_confirm_delete.html', {'staff': staff})


@role_required('platform_superuser', 'super_admin', 'admin')
def leave_list(request):
    leaves = LeaveApplication.objects.all().order_by('-created_at')
    return render(request, 'staff/leave_list.html', {'leaves': leaves})


@role_required('platform_superuser', 'super_admin', 'admin', 'teacher')
def leave_apply(request):
    if request.method == 'POST':
        try:
            leave = LeaveApplication(
                staff=Staff.objects.get(user=request.user),
                leave_type=LeaveType.objects.get(pk=request.POST.get('leave_type')),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                reason=request.POST.get('reason'),
            )
            leave.save()
            messages.success(request, 'Leave application সফলভাবে submit হয়েছে।')
            return redirect('staff:leave_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    leave_types = LeaveType.objects.filter(is_active=True)
    return render(request, 'staff/leave_form.html', {'leave_types': leave_types})