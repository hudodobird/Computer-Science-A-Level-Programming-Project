from django.urls import path
from . import views

urlpatterns = [
    path('homework/', views.homework, name='homework'),
    path('homework/<int:pk>/', views.homework_detail, name='homework_detail'),
    path('homework/<int:pk>/submit/', views.submit_homework, name='submit_homework'),
]