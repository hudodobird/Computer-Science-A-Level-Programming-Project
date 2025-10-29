from django.db import models
from django.conf import settings


class TutorialProgress(models.Model):
	"""Tracks per-user completion state for a tutorial section.

	A section is identified by its slug (string) to keep things simple.
	We track completion of two steps: example and question.
	"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tutorial_progress")
	section_slug = models.SlugField(max_length=100, db_index=True)
	completed_example = models.BooleanField(default=False)
	completed_question = models.BooleanField(default=False)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ("user", "section_slug")

	def __str__(self) -> str:
		return f"{self.user} • {self.section_slug} (ex={self.completed_example}, q={self.completed_question})"

# Create your models here.
