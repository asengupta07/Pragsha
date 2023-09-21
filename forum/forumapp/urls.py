from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum, name='forumapp'),
    path('create_thread/', views.create_thread, name='create_thread'),
    path('thread_detail/', views.thread_detail, name='thread_detail'),
]