from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # link UserProfile to django User model instance
    user = models.OneToOneField(User)
    
    # additional attributes
    #
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    def __str__(self):
        return self.user.username