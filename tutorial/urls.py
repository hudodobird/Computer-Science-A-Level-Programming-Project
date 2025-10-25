from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutorial_home, name='tutorial_home'),
    path('<slug:slug>/', views.tutorial_section, name='tutorial_section'),
]
