from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('homework/', views.homework, name='homework'),
]