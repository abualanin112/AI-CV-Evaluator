from django.contrib import admin
from .models import JobDescription, CV

@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'created_at')

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'candidate_email', 'fit_score', 'created_at')
    list_filter = ('job', 'created_at')
