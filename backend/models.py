from django.db import models
from django.contrib.auth.models import User 

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    prompt = models.TextField(max_length=1000)
    refraim = models.TextField(max_length=1000)
    conclusion = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.prompt