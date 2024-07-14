import uuid
from django.db import models


class Project(models.Model):
    project_key = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=500)
    tags = models.CharField(max_length=500)
    cover_image = models.FileField(upload_to='real-estate-images')
    client = models.TextField()
    project_date = models.DateField(null=True)
    description = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Images(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='real-estate-images')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
