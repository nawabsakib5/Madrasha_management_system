from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import (
    FeeCategory, FeeStructure, FeeInvoice,
    FeePayment, CashBookEntry, SalaryStructure, SalaryPayment
)
from apps.students.models import Student
import uuid


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


# ─── Fee Category ─────────────────────────────────────────
@role_required('platform_superuser', 'super_admin', 'admin', 'accountant')
def fee_category_list(request):
    categories = FeeCategory.objects.filter(is_active=True)
    return render(request, 'accounting/fee_category_list.html', {'categories': categories})


@role_required('platform_superuser', 'super_admin', 'admin', 'accountant')
def fee_category_add(request):
    if request.method == 'POST':
        try:
            category = FeeCategory(
                name=request.POST.get('name'),
                description=request.POST.get('description', ''),
            )
            category.save()
            messages.success(request, f'Fee Category {category.name} সফলভাবে যোগ করা হয়েছে।')
            return redirect('accounting:fee_category_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request, 'accounting/fee_category_form.html', {'action': 'Add'})


# ─── Fee Invoice ──────────────────────────────────────────
@role_required('platform_superuser', 'super_admin', 'admin', 'accountant')
def fee_invoice_list(request):
    invoices = FeeInvoice.objects.all().order_by('-created_at')
    return render(request, 'accounting/fee_invoice_list.html', {'invoices': invoices})


@role_required('platform_superuser', 'super_admin', 'admin', 'accountant')
def fee_invoice_add(request):
    if request.method == 'POST':
        try:
            invoice = FeeInvoice(
                student=Student.objects.get(pk=request.POST.get('student')),
                category=FeeCategory.objects.get(pk=request.POST.get('category')),
                amount=request.POST.get('amount'),
                due_date=request.POST.get('due_date'),
                month=request.POST.get('month') or None,
                year=request.POST.get('year') or None,
            )
            invoice.save()
            messages.success(request, 'Invoice সফলভাবে তৈরি হয়েছে।')
            return redirect('accounting:fee_invoice_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    students = Student.objects.filter(is_active=True)
    categories = FeeCategory.objects.filter(is_active=True)
    return render(request, 'accounting/fee_invoice_form.html', {
        'action': 'Add',
        'students': students,
        'categories': categories,
    })


# ─── Fee Payment ──────────────────────────────────────────
@role_required('platform_superuser', 'super_admin', 'admin', 'accountant')
def fee_payment_list(request):
    payments = FeePayment.objects.filter(is_void=False).order_by('-paid_at')
    return render(request, 'accounting/fee_payment_list.html', {'payments': payments})


@role_required('platform_superuser', 'super_admin', 'admin', 'accountant')
def fee_payment_add(request, invoice_pk):
    invoice = get_object_or_404(FeeInvoice, pk=invoice_pk)
    if request.method == 'POST':
        try:
            receipt_no = f'RCP-{uuid.uuid4().hex[:8].upper()}'
            payment = FeePayment(
                invoice=invoice,
                amount_paid=request.POST.get('amount_paid'),
                method=request.POST.get('method'),
                receipt_no=receipt_no,
                received_by=request.user,
            )
            payment.save()

            # Update invoice status
            total_paid = sum(p.amount_paid for p in invoice.payments.filter(is_void=False))
            if total_paid >= invoice.amount:
                invoice.status = 'paid'
            else:
                invoice.status = 'partial'
            invoice.save()

            messages.success(request, f'Payment সফলভাবে রেকর্ড হয়েছে। Receipt: {receipt_no}')
            return redirect('accounting:fee_payment_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'accounting/fee_payment_form.html', {
        'invoice': invoice,
        'method_choices': FeePayment.METHOD_CHOICES,
    })


# ─── Cash Book ────────────────────────────────────────────
@role_required('platform_superuser', 'super_admin', 'admin', 'accountant')
def cashbook_list(request):
    entries = CashBookEntry.objects.all().order_by('-date')
    total_income = sum(e.amount for e in entries if e.type == 'income')
    total_expense = sum(e.amount for e in entries if e.type == 'expense')
    balance = total_income - total_expense
    return render(request, 'accounting/cashbook_list.html', {
        'entries': entries,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    })


@role_required('platform_superuser', 'super_admin', 'admin', 'accountant')
def cashbook_add(request):
    if request.method == 'POST':
        try:
            entry = CashBookEntry(
                date=request.POST.get('date'),
                type=request.POST.get('type'),
                category=request.POST.get('category'),
                amount=request.POST.get('amount'),
                description=request.POST.get('description', ''),
                reference=request.POST.get('reference', ''),
                recorded_by=request.user,
            )
            entry.save()
            messages.success(request, 'Cash Book Entry সফলভাবে যোগ হয়েছে।')
            return redirect('accounting:cashbook_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'accounting/cashbook_form.html', {'action': 'Add'})