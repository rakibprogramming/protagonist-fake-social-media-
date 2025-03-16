from django.db import models

# Create your models here.
class posts(models.Model):
    userId = models.CharField(max_length=200)
    postId = models.CharField(max_length=10)
    text = models.CharField(max_length=10000)
    hasImage = models.CharField(max_length=1)

class user(models.Model):
    userId = models.CharField(max_length=200)
    sessonId = models.CharField(max_length=100)
    userName = models.CharField(max_length=200) 