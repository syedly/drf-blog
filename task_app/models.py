from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    def __str__(self):
        return self.user.username
    
class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    liked_by = models.ManyToManyField(User, related_name='liked_by', blank=True)
    
    def total_likes(self):
        return self.liked_by.count()

    def __str__(self):
        return self.user.username
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.TextField()
    
    def __str__(self):
        return f"{self.user}comment on {self.blog}"