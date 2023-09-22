from django.urls import path
from . import views

app_name = 'agency'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('inventory/', views.add_inventory, name='inventory'),
]