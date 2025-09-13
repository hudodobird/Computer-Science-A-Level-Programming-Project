from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try some other username")
            return render(request, 'accounts/signup.html')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return render(request, 'accounts/signup.html')

        if len(username) > 50:
            messages.error(request, "Username must be under 50 characters")

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")

        if not username.isalnum():
            messages.error(request, "Username must be letters or numbers!")

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Account successfully created.")
        return redirect('home')
    return render(request, 'accounts/signup.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
