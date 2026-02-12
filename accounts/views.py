from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from .forms import SignUpForm
from pastpapers.models import QuestionCompletion
from homework.models import Submission
from tutorial.models import TutorialProgress

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # Deactivate until they click the link
            user.save()
            
            # Application Email Verification Logic
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = current_site.domain
            
            # Construct the link manually for the email
            # We also print it to the terminal for easier testing in Codespaces
            link = f"http://{domain}/accounts/activate/{uid}/{token}/"
            print(f"\n\n--- ACTIVATION LINK ---\n{link}\n-----------------------\n")

            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': domain,
                'uid': uid,
                'token': token,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )

            email.send()
            

            messages.success(request, "Please confirm your email address to complete the registration. Check your specific email inbox (or the terminal if testing).")
            return redirect('login') # Redirect to login page instead of home so they know what to do next
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        
        # Auto-login the user
        login(request, user)
        
        messages.success(request, 'Account activated! You are now logged in.')
        return redirect('profile')
    else:
        messages.error(request, 'Activation link is invalid or expired!')
        return redirect('login')

@login_required
def profile(request):
    # Past Papers Progress
    questions_completed = QuestionCompletion.objects.filter(user=request.user, completed=True)
    questions_count = questions_completed.count()

    # Homework Progress
    submissions = Submission.objects.filter(student=request.user).order_by('-submitted_at')

    # Tutorial Progress
    tutorials = TutorialProgress.objects.filter(user=request.user)
    tutorials_completed_count = tutorials.filter(completed_example=True, completed_question=True).count()

    context = {
        'user': request.user,
        'questions_count': questions_count,
        'recent_questions': questions_completed.order_by('-updated_at')[:5],
        'submissions': submissions,
        'tutorials_completed_count': tutorials_completed_count,
        'recent_tutorials': tutorials.order_by('-updated_at')[:5],
    }
    return render(request, 'accounts/profile.html', context)
