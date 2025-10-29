from django.contrib import admin
from .models import TutorialProgress


@admin.register(TutorialProgress)
class TutorialProgressAdmin(admin.ModelAdmin):
	list_display = ("user", "section_slug", "completed_example", "completed_question", "updated_at")
	list_filter = ("completed_example", "completed_question")
	search_fields = ("user__username", "section_slug")
