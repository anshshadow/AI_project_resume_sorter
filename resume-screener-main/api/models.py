from django.db import models
from django.contrib.auth.models import User

class JobDescription(models.Model):
    hr = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Resume(models.Model):
    job_description = models.ForeignKey(JobDescription, related_name='resumes', on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    name = models.CharField(max_length=255)
    score = models.FloatField(default=0.0)
    remarks = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} for {self.job_description.title}"
