from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('audit-log/', views.audit_log_view, name='audit_log'),
]