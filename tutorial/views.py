from django.shortcuts import render
from django.http import Http404


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
	sections = [
		{"title": "Python Basics", "slug": "python-basics", "prompt": "Print 'Hello, world!' and assign a variable called name with your name."},
		{"title": "Conditionals", "slug": "conditionals", "prompt": "Ask for a number and print whether it is positive, negative, or zero."},
		{"title": "Loops", "slug": "loops", "prompt": "Use a for loop to print numbers 1 through 10."},
		{"title": "Functions", "slug": "functions", "prompt": "Write a function add(a, b) that returns their sum and test it."},
		{"title": "Lists & Dictionaries", "slug": "lists-and-dicts", "prompt": "Create a list of three fruits and a dict mapping fruit to color. Print both."},
		{"title": "File I/O", "slug": "file-io", "prompt": "Write text to a file named notes.txt then read it back and print its contents."},
	]
	return render(request, 'tutorial.html', {"sections": sections})


def tutorial_section(request, slug: str):
	sections = {
		"python-basics": {
			"title": "Python Basics",
			"prompt": "Print 'Hello, world!' and assign a variable called name with your name.",
			"starter": "# Your code here\nprint('Hello, world!')\nname = 'Radnor'\nprint('Name:', name)\n",
		},
		"conditionals": {
			"title": "Conditionals",
			"prompt": "Ask for a number and print whether it is positive, negative, or zero.",
			"starter": "n = int(input('Enter a number: '))\nif n > 0:\n    print('positive')\nelif n < 0:\n    print('negative')\nelse:\n    print('zero')\n",
		},
		"loops": {
			"title": "Loops",
			"prompt": "Use a for loop to print numbers 1 through 10.",
			"starter": "for i in range(1, 11):\n    print(i)\n",
		},
		"functions": {
			"title": "Functions",
			"prompt": "Write a function add(a, b) that returns their sum and test it.",
			"starter": "def add(a, b):\n    return a + b\n\nprint(add(2, 3))\n",
		},
		"lists-and-dicts": {
			"title": "Lists & Dictionaries",
			"prompt": "Create a list of three fruits and a dict mapping fruit to color. Print both.",
			"starter": "fruits = ['apple', 'banana', 'cherry']\ncolors = {'apple': 'red', 'banana': 'yellow', 'cherry': 'red'}\nprint(fruits)\nprint(colors)\n",
		},
		"file-io": {
			"title": "File I/O",
			"prompt": "Write text to a file named notes.txt then read it back and print its contents.",
			"starter": "with open('notes.txt', 'w') as f:\n    f.write('Hello file!')\nwith open('notes.txt') as f:\n    print(f.read())\n",
		},
	}

	data = sections.get(slug)
	if not data:
		raise Http404("Tutorial section not found")

	return render(request, 'tutorial_section.html', data | {"slug": slug})
