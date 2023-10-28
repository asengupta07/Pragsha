from django.urls import path
from . import views

urlpatterns = [
    path('forum/', views.dashboard, name='dashboard'),
    path('get_queries/', views.get_queries, name='get_queries'),
    path('sos/', views.sos, name='sos'),
    path('broadcast/', views.broadcast, name='broadcast'),
    path('get_response/', views.get_response, name='get_response'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('dashboard/', views.map, name='map'),
]
