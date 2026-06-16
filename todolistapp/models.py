from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class UserModel(AbstractBaseUser):
    
    
    def __str__(self):
        return self.username
    

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
