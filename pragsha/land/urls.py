from django.urls import path
from . import views

app_name = 'land'
urlpatterns = [
    path('', views.landing, name='home'),
    path('faq/', views.faq, name='faq'),
]