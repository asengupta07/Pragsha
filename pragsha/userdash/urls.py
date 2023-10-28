from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('get_queries/', views.get_queries, name='get_queries'),
]