from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutorial_home, name='tutorial_home'),
    path('<slug:slug>/', views.tutorial_section, name='tutorial_section'),
    path('api/progress/<slug:slug>/<str:step>/', views.update_progress, name='tutorial_update_progress'),
]
