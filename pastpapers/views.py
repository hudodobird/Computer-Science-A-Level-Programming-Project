from collections import defaultdict
from django.shortcuts import render
from .models import Question


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

