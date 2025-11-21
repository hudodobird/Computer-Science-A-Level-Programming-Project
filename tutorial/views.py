from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import TutorialProgress


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
			"starter": "# Write your code here\n",
			"answer": "print('Hello, world!')\nname = 'Jim'\nprint('Name:', name)\n",
			"example_text": "This example prints a greeting and a variable value. Variables are used to store data, such as string or numbers. In the example code, the variable name is assigned to the string 'Alex' using the = operator. Variables can be reused as many times as needed and can be changed too.",
			"example_code": "print('Hello, world!')\nname = 'Alex'\nprint('Name:', name)\n",
		},
		"conditionals": {
			"title": "Conditionals",
			"prompt": "Ask for a number and print whether it is positive, negative, or zero.",
			"starter": "# Write your code here\n",
			"answer": "x = float(input('Enter a number: '))\nif x > 0:\n    print('positive')\nelif x < 0:\n    print('negative')\nelse:\n    print('zero')\n",
			"example_text": "Conditionals choose different code paths based on a condition. And example would be an if statement. If statements decide whether their condition is true or false, the example decides whether a number is positive or negative. If the number is a whole number when divided by 2, it's positive, otherwise it will always be negative.",
			"example_code": "x = 5\nif x % 2 == 0:\n    print('even')\nelse:\n    print('odd')\n",
		},
		"loops": {
			"title": "Loops",
			"prompt": "Use a for loop to print numbers 1 through 10 with a step of 2.",
			"starter": "# Write your code here\n",
			"answer": "for i in range(1, 11, 2):\n    print(i)\n",
			"example_text": "A for loop repeats an action as many times as it's called. i is a common name used in for loops to represent the current iteration value, the first time the loop runs i will be 0, the second time it will be 1 and so on, up to but not including the end value of 5.\n The range() operation uses a specific formant for inside the (), range(start, stop, step) step being what value it increments by.",
			"example_code": "for i in range(1, 25, 1):\n    print(i)",
		},
		"functions": {
			"title": "Functions",
			"prompt": "Write a function add(a, b) that returns their sum and test it.",
			"starter": "# Write your code here\n",
			"answer": "def add(a, b):\n    return a + b\n\nprint(add(2, 3))\n",
			"example_text": "Functions are sections of code that can be reused multiple times. This example defines a function (def) called greet(), the brackets pass through variables that are used inside the function. As name is assigned to 'Sam' when greet() is called, it prints 'Hello, Sam'.",
			"example_code": "def greet(name):\n    print('Hello,', name)\n\ngreet('Sam')\n",
		},
		"lists-and-dicts": {
			"title": "Lists & Dictionaries",
			"prompt": "Create a list of three fruits and a dict mapping fruit to color. Print both.",
			"starter": "# Write your code here\n",
			"answer": "fruits = ['apple', 'banana', 'cherry']\ncolors = {'apple': 'red', 'banana': 'yellow', 'cherry': 'red'}\nprint(fruits)\nprint(colors)\n",
			"example_text": "Lists order multiple items together. The first value inside a list starts at index 0, the second at index 1 and so on. Dictionaries map keys to values, for example fruits to colours or cars to colours. In this example, a list of numbers and a dictionary mapping people's names and ages.",
			"example_code": "nums = [1, 2, 3]\nuser = {'name': 'Taylor', 'age': 15}\nprint(nums)\nprint(user['name'])\n",
		},
		"file-io": {
			"title": "File I/O",
			"prompt": "Write text to a file named notes.txt then read it back and print its contents.",
			"starter": "# Write your code here\n",
			"answer": "with open('notes.txt', 'w') as f:\n    f.write('Some notes...')\n\nwith open('notes.txt') as f:\n    print(f.read())\n",
			"example_text": "Python files can access data from other files. This example opens the file to write to (hence the w) and writes the string 'Hi!'. Then the file is opened again for reading and is read.",
			"example_code": "with open('example.txt', 'w') as f:\n    f.write('Hi!')\nwith open('example.txt') as f:\n    print(f.read())\n",
		},
	}

	data = sections.get(slug)
	if not data:
		raise Http404("Tutorial section not found")

	# Progress for the current user
	completed_example = False
	completed_question = False
	if request.user.is_authenticated:
		progress, _ = TutorialProgress.objects.get_or_create(user=request.user, section_slug=slug)
		completed_example = progress.completed_example
		completed_question = progress.completed_question

	context = data | {
		"slug": slug,
		"completed_example": completed_example,
		"completed_question": completed_question,
	}
	return render(request, 'tutorial_section.html', context)


@login_required
@require_POST
def update_progress(request, slug: str, step: str):
	"""Toggle or set completion for a given step (example|question).

	Request body (JSON): {"completed": true|false}
	"""
	if step not in {"example", "question"}:
		return JsonResponse({"error": "invalid step"}, status=400)

	try:
		import json
		payload = json.loads(request.body or b"{}")
		completed = bool(payload.get("completed"))
	except Exception:
		return JsonResponse({"error": "invalid json"}, status=400)

	progress, _ = TutorialProgress.objects.get_or_create(user=request.user, section_slug=slug)
	if step == "example":
		progress.completed_example = completed
	else:
		progress.completed_question = completed
	progress.save()

	return JsonResponse({
		"slug": slug,
		"step": step,
		"completed": completed,
		"completed_example": progress.completed_example,
		"completed_question": progress.completed_question,
	})
