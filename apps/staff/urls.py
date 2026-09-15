from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.staff_list, name='staff_list'),
    path('<int:pk>/', views.staff_detail, name='staff_detail'),
    path('add/', views.staff_add, name='staff_add'),
    path('<int:pk>/edit/', views.staff_edit, name='staff_edit'),
    path('<int:pk>/delete/', views.staff_delete, name='staff_delete'),
    path('leave/', views.leave_list, name='leave_list'),
    path('leave/apply/', views.leave_apply, name='leave_apply'),
]