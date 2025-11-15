from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ("year", "question_number", "difficulty", "created_at")
	list_filter = ("year", "difficulty")
	search_fields = ("question_number",)
	ordering = ("-year", "question_number")

