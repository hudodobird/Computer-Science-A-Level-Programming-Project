from django.db import models


class Question(models.Model):
	class Difficulty(models.TextChoices):
		EASY = "easy", "Easy"
		MEDIUM = "medium", "Medium"
		HARD = "hard", "Hard"

	year = models.PositiveIntegerField()
	question_number = models.CharField(max_length=10)
	difficulty = models.CharField(
		max_length=10,
		choices=Difficulty.choices,
		default=Difficulty.MEDIUM,
		help_text="Relative difficulty of the question",
	)
	image = models.ImageField(upload_to="pastpapers/questions/%Y/%m/%d/", null=True, blank=True)
	image_2 = models.ImageField(
		upload_to="pastpapers/questions/%Y/%m/%d/",
		null=True,
		blank=True,
		verbose_name="Second Image (Optional)"
	)
	answer_text = models.TextField(blank=True)
	starter_code = models.TextField(blank=True, default="# Write your code here")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=["year", "question_number"], name="uq_year_question_number"
			)
		]
		ordering = ["-year", "question_number"]

	def __str__(self) -> str:
		return f"{self.year} Q{self.question_number} ({self.get_difficulty_display()})"


class QuestionCompletion(models.Model):
	user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="question_completions")
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="completions")
	completed = models.BooleanField(default=False)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ("user", "question")

	def __str__(self):
		status = "Done" if self.completed else "In Progress"
		return f"{self.user.username} - {self.question} ({status})"

