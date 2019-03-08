from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_images', blank=True)
    register_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class Recipe(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    url = models.CharField(max_length=200)

class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    text = models.TextField()