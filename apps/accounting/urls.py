from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    # Fee Category
    path('fee-category/', views.fee_category_list, name='fee_category_list'),
    path('fee-category/add/', views.fee_category_add, name='fee_category_add'),

    # Fee Invoice
    path('fee-invoice/', views.fee_invoice_list, name='fee_invoice_list'),
    path('fee-invoice/add/', views.fee_invoice_add, name='fee_invoice_add'),

    # Fee Payment
    path('fee-payment/', views.fee_payment_list, name='fee_payment_list'),
    path('fee-payment/add/<int:invoice_pk>/', views.fee_payment_add, name='fee_payment_add'),

    # Cash Book
    path('cashbook/', views.cashbook_list, name='cashbook_list'),
    path('cashbook/add/', views.cashbook_add, name='cashbook_add'),
]