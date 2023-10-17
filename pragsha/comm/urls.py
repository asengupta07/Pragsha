from django.urls import path
from . import views

app_name = 'comm'
urlpatterns = [
    path('', views.chat, name='chat'),
]