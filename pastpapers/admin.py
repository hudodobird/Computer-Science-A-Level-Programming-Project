from django.contrib import admin
from .models import Question, QuestionCompletion


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ("year", "question_number", "difficulty", "created_at")
	list_filter = ("year", "difficulty")
	search_fields = ("question_number",)
	ordering = ("-year", "question_number")


@admin.register(QuestionCompletion)
class QuestionCompletionAdmin(admin.ModelAdmin):
	list_display = ("user", "question", "completed", "updated_at")
	list_filter = ("completed", "updated_at")
	search_fields = ("user__username", "question__question_number")


