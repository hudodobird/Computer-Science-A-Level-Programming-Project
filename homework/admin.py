from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import HomeworkTemplate, Assignment, Submission

@admin.register(HomeworkTemplate)
class HomeworkTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'due_date', 'created_at')
    list_filter = ('group', 'due_date')
    search_fields = ('title', 'group__name')
    fieldsets = (
        (None, {
            'fields': ('group', 'source_template', 'due_date')
        }),
        ('Content (Auto-filled from template if left blank)', {
            'fields': ('title', 'description', 'starter_code'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'submitted_at', 'view_code_link')
    list_filter = ('assignment', 'submitted_at')
    search_fields = ('student__username', 'assignment__title')
    readonly_fields = ('student', 'assignment', 'code', 'submitted_at')

    def view_code_link(self, obj):

        url = reverse("admin:homework_submission_change", args=[obj.id])
        return format_html('<a href="{}">View Code</a>', url)
    
    view_code_link.short_description = "Code"
