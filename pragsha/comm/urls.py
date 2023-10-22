from django.urls import path
from . import views

app_name = 'comm'
urlpatterns = [
    path('', views.chat, name='chat'),
    path('create', views.create, name='create'),
    path('update', views.update, name='update'),
]