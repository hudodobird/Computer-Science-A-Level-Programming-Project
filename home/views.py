from django.shortcuts import render, redirect

# Create your views here.

def home(request):

    return render(request, 'index.html')


def redirect_to_home(request):
    return redirect('home')