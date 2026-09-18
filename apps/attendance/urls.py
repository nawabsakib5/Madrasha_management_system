from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Student Attendance
    path('student/', views.student_attendance_list, name='student_attendance_list'),
    path('student/mark/', views.student_attendance_mark, name='student_attendance_mark'),

    # Staff Attendance
    path('staff/', views.staff_attendance_list, name='staff_attendance_list'),
    path('staff/mark/', views.staff_attendance_mark, name='staff_attendance_mark'),
    path('staff/import/', views.staff_attendance_import, name='staff_attendance_import'),
]