from django.urls import path
from . import views

app_name = 'pastpapers'

urlpatterns = [
    path('', views.questions_list, name='questions'),
]
