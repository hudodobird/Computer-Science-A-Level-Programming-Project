from django.db import models
from django.contrib.auth.models import Group, User

class HomeworkTemplate(models.Model):
    """A reusable template for homework assignments."""
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Instructions for the students")
    starter_code = models.TextField(default="# Write your code here", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    """A specific homework task assigned to a group of students."""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="assignments")
   
    source_template = models.ForeignKey(HomeworkTemplate, on_delete=models.SET_NULL, null=True, blank=True, help_text="Select a template to auto-fill fields")
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    starter_code = models.TextField(default="# Write your code here", blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.source_template and not self.title:
            self.title = self.source_template.title
            self.description = self.source_template.description
            self.starter_code = self.source_template.starter_code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.group.name}"

class Submission(models.Model):
    """A student's submission for an assignment."""
    STATUS_CHOICES = [
        ('draft', 'In Progress'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]
    
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="homework_submissions")
    code = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    grade = models.CharField(max_length=10, blank=True, help_text="e.g. A, 8/10, Pass")
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"
