from django.db import models
from django.contrib.auth.models import User 

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    prompt = models.TextField(max_length=300)
    refraim = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)