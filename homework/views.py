from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Assignment, Submission
import json

@login_required
def homework(request):
    
    user_groups = request.user.groups.all()
    
    assignments = Assignment.objects.filter(group__in=user_groups).order_by('-due_date')
    
    submissions = Submission.objects.filter(student=request.user, assignment__in=assignments)
    submission_map = {s.assignment_id: s for s in submissions}

    for a in assignments:
        sub = submission_map.get(a.id)
        a.user_status = sub.status if sub else 'todo'
        a.user_grade = sub.grade if sub else ''

    return render(request, 'homework.html', {
        'assignments': assignments,
    })

@login_required
def homework_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    
    if not request.user.groups.filter(pk=assignment.group.pk).exists():
        return redirect('homework')

    submission, created = Submission.objects.get_or_create(
        assignment=assignment,
        student=request.user,
        defaults={'code': assignment.starter_code}
    )

    return render(request, 'homework_detail.html', {
        'assignment': assignment,
        'submission': submission,
    })

@login_required
@require_POST
def submit_homework(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    
    try:
        data = json.loads(request.body)
        code = data.get('code', '')
        action = data.get('action', 'save') 
    except:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    submission, _ = Submission.objects.get_or_create(
        assignment=assignment,
        student=request.user
    )
    
    submission.code = code
    if action == 'submit':
        submission.status = 'submitted'
    
    submission.save()
    
    return JsonResponse({
        'status': submission.status,
        'message': 'Saved' if action == 'save' else 'Submitted successfully'
    })
