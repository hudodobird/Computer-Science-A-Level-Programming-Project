from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Question, QuestionCompletion


def questions_list(request):
	qs = Question.objects.all().order_by('-year', 'question_number')

	groups = []
	if qs.exists():
		grouped = defaultdict(list)
		for q in qs:
			grouped[q.year].append(q)
		for year in sorted(grouped.keys(), reverse=True):
			groups.append({
				'year': year,
				'questions': grouped[year],
			})
	else:
		groups = [
			{
				'year': 2024,
				'questions': [
					{'question_number': '1', 'difficulty': 'easy'},
					{'question_number': '2', 'difficulty': 'medium'},
					{'question_number': '3', 'difficulty': 'hard'},
				],
			},
			{
				'year': 2023,
				'questions': [
					{'question_number': '1a', 'difficulty': 'medium'},
					{'question_number': '1b', 'difficulty': 'hard'},
					{'question_number': '2', 'difficulty': 'easy'},
				],
			},
		]

	return render(request, 'pastpapers/questions.html', {
		'groups': groups,
	})


def question_detail(request, pk):
	question = get_object_or_404(Question, pk=pk)
	is_completed = False
	if request.user.is_authenticated:
		completion = QuestionCompletion.objects.filter(user=request.user, question=question).first()
		if completion:
			is_completed = completion.completed
	
	return render(request, 'pastpapers/detail.html', {
		'question': question,
		'is_completed': is_completed,
	})


@login_required
@require_POST
def update_completion(request, pk):
	"""Toggle completion status for a question."""
	question = get_object_or_404(Question, pk=pk)
	
	try:
		import json
		payload = json.loads(request.body or b"{}")
		completed = bool(payload.get("completed"))
	except Exception:
		return JsonResponse({"error": "invalid json"}, status=400)

	completion, _ = QuestionCompletion.objects.get_or_create(user=request.user, question=question)
	completion.completed = completed
	completion.save()

	return JsonResponse({
		"pk": pk,
		"completed": completion.completed,
	})

