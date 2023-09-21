from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.map_view, name='map_view'),
]
