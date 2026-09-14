from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.core.models import LoginAttempt


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Login attempt log
            LoginAttempt.objects.create(
                username_attempted=username,
                user=user,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                success=True,
            )

            # Force password change check
            if user.must_change_password:
                return redirect('accounts:change_password')

            return redirect('core:dashboard')

        else:
            # Failed login attempt log
            LoginAttempt.objects.create(
                username_attempted=username,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                success=False,
            )
            messages.error(request, 'Username অথবা Password ভুল হয়েছে।')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def change_password_view(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            messages.error(request, 'পুরনো Password ভুল।')
        elif new_password != confirm_password:
            messages.error(request, 'নতুন Password মিলছে না।')
        elif len(new_password) < 10:
            messages.error(request, 'Password কমপক্ষে ১০ অক্ষরের হতে হবে।')
        else:
            request.user.set_password(new_password)
            request.user.must_change_password = False
            request.user.save()
            messages.success(request, 'Password সফলভাবে পরিবর্তন হয়েছে।')
            return redirect('accounts:login')

    return render(request, 'accounts/change_password.html')