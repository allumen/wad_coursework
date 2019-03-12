from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_images', blank=True)
    register_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=200)

    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    url = models.CharField(max_length=200, unique=True)
    
    date_created = models.DateField(auto_now_add=True)
    public = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
        
        
class Recipe(Post):
    preparations = models.TextField(blank=True)
    instructions = models.TextField()
    
    
class Tip(Post):
    text = models.TextField()
    
    
class Ingridient(models.Model):
    pass

    
class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    text = models.TextField()
