from django.shortcuts import render

# Create your views here.

def home(request):

    return render(request, 'index.html')


def homework(request):

    return render(request, 'homework.html')