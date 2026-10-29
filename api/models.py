from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class ReadingMaterials(models.Model):
    title = models.TextField(blank=True, null=True)
    difficulty = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    
    date_added = models.DateTimeField(auto_now_add=True)
    

class Ratings(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    material_title = models.ForeignKey(ReadingMaterials, on_delete=models.CASCADE)
    rate = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
   
    
    created = models.DateTimeField(auto_now_add=True)