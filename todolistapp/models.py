from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    # 👇 Fix this line here: change on_state to on_delete
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)  # Also double check it says max_length, not max_state!
    description = models.TextField(blank=True, null=True) 
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title