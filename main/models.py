from django.db import models

# Create your models here.
class posts(models.Model):
    userId = models.CharField(max_length=200)
    postId = models.CharField(max_length=10)
    text = models.CharField(max_length=10000)
    hasImage = models.CharField(max_length=1)
    time = models.CharField(max_length=30, default="1742224146.9047246")

class user(models.Model):
    userId = models.CharField(max_length=200)
    sessonId = models.CharField(max_length=100)
    userName = models.CharField(max_length=200) 

class comment(models.Model):
    commentText = models.CharField(max_length=1000)
    postId = models.CharField(max_length=10, db_index=True)
    commentId = models.CharField(max_length=10)
    time = models.CharField(max_length=30, default="1742224146.9047246")
    userId = models.CharField(max_length=200, default="none")
    userName = models.CharField(max_length=200, default="none")


class likes(models.Model):
    userId = models.CharField(max_length=100)
    postId = models.CharField(max_length=10, db_index=True)