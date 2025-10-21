from django.shortcuts import render


def tutorial_home(request):
	sections = [
		{"title": "Python Basics"},
		{"title": "Loops"},
		{"title": "If Statements"},
		{"title": "Functions"},
		{"title": "Sorting"},
		{"title": "Error messages"},
        {"title": "Turtle"},
		{"title": "File I/O"},
	]
	return render(request, 'tutorial.html', {"sections": sections})
