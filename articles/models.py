from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

class Score(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scores')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()  # 0 to 5
    updated_at = models.DateTimeField(auto_now=True)  # For cooldown checks
