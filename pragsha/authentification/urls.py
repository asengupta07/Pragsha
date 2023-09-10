from django.urls import path
from . import views

app_name = 'authentification'
urlpatterns = [
    path('register/', views.register, name='register')
]