from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dash, name='map_view'),
    path('dashboard/response/', views.response, name='dash'),
    path('dashboard/drone/', views.drone, name='drone')
]
