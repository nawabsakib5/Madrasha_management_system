from django.urls import path
from . import views

app_name = 'examination'

urlpatterns = [
    # Exam
    path('', views.exam_list, name='exam_list'),
    path('add/', views.exam_add, name='exam_add'),

    # Result
    path('result/', views.result_list, name='result_list'),
    path('result/add/<int:exam_pk>/', views.result_add, name='result_add'),

    # Admit Card
    path('admit-card/', views.admit_card_list, name='admit_card_list'),
    path('admit-card/generate/<int:exam_pk>/', views.admit_card_generate, name='admit_card_generate'),
]