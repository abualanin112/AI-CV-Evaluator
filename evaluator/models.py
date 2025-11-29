from django.db import models
import json

class JobDescription(models.Model):
    job_title = models.CharField(max_length=200)
    job_requirements = models.TextField(help_text="Enter the job description and requirements here.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title

class CV(models.Model):
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE, related_name='cvs', null=True, blank=True)
    file = models.FileField(upload_to='cvs/')
    candidate_name = models.CharField(max_length=200, blank=True, null=True)
    candidate_email = models.EmailField(blank=True, null=True)
    raw_text = models.TextField(blank=True)
    evaluation_json = models.JSONField(blank=True, null=True)
    fit_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.candidate_name or f"CV {self.id}"
