from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import HomeworkTemplate, Assignment, Submission, TestCase

class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1

@admin.register(HomeworkTemplate)
class HomeworkTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)

from django import forms

class AssignmentAdminForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make these fields optional in the form so auto-fill can handle them
        # if the user selects a template but leaves them blank.
        self.fields['title'].required = False
        self.fields['description'].required = False
        self.fields['starter_code'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        source_template = cleaned_data.get('source_template')
        
        # If no template is selected, title is mandatory
        if not source_template and not title:
            self.add_error('title', 'Title is required if no template is selected.')
            
        return cleaned_data

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    form = AssignmentAdminForm
    list_display = ('title', 'group', 'due_date', 'created_at')
    
    class Media:
        js = ('homework/admin_assignment.js',) # Needs to be served by staticfiles

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
    inlines = [TestCaseInline]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'submitted_at', 'status', 'manual_review_requested', 'view_code_link')
    list_filter = ('assignment', 'submitted_at', 'status', 'manual_review_requested')
    search_fields = ('student__username', 'assignment__title')
    readonly_fields = ('student', 'assignment', 'code', 'submitted_at')

    def view_code_link(self, obj):

        url = reverse("admin:homework_submission_change", args=[obj.id])
        return format_html('<a href="{}">View Code</a>', url)
    
    view_code_link.short_description = "Code"
