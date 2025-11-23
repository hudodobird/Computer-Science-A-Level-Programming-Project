from django.urls import path
from . import views

app_name = 'pastpapers'

urlpatterns = [
    path('', views.questions_list, name='questions'),
    path('<int:pk>/', views.question_detail, name='detail'),
    path('api/completion/<int:pk>/', views.update_completion, name='update_completion'),
]
