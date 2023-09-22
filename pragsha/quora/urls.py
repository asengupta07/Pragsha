# quora_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('question_list/', views.question_list, name='question_list'),
    path('question_detail/', views.question_detail, name='question_detail'),
]
