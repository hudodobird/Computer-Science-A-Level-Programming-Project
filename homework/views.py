from django.shortcuts import render

# Create your views here.

def homework(request):

    return render(request, 'homework.html')