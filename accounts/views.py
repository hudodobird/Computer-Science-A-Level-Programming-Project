from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from pastpapers.models import QuestionCompletion
from homework.models import Submission
from tutorial.models import TutorialProgress

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account successfully created.")
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

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
