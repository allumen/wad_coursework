from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import datetime 
import os

def recipe_image_handler(instance, filename):   
    # get new file extension and save with custom name
    image_extension = os.path.splitext(filename)[1]
    new_name = '/'.join(['recipe_images', instance.title, str(instance.url) + image_extension])
    return '/'.join(['recipe_images', instance.title, str(instance.url) + image_extension])


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_images', blank=True)
    register_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username


class RecipeCategory(models.Model):
    title = models.CharField(primary_key=True, max_length=128)
    description = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.title 
       

class Recipe(models.Model):
    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=200)
    # user custom upload_to callable to rename uploaded images
    image = models.ImageField(upload_to=recipe_image_handler, blank=True)
    
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    url = models.CharField(max_length=200, unique=True)
    url_chosen = models.BooleanField(default=False)
    
    date_created = models.DateField(auto_now_add=True)
    public = models.BooleanField(default=False)
    likes = models.ManyToManyField(UserProfile, blank=True, related_name="likes")
    
    objects = models.Manager()
    
    description = models.CharField(max_length=300, blank=True)
    instructions = models.TextField()
    categories = models.ManyToManyField(RecipeCategory, blank=True)
    
    # recipe details
    preparation_time = models.PositiveIntegerField()
    servings_number = models.PositiveIntegerField()
    
    def save(self, *args, **kwargs):    
        if not self.url_chosen:
            url_variant = slugify(self.title + " " + str(datetime.now().date()))
            
            # avoid url collisions by appending an int if the url exists already
            same_urls = Recipe.objects.filter(url__contains=url_variant)
            if len(same_urls) > 0:
                url_variant = "{}-{}".format(url_variant, len(same_urls))
                
            self.url = url_variant
            self.url_chosen = True
            
        super(Recipe, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(max_length=128, blank=False)
    quantity = models.PositiveIntegerField()
    
    units = models.ForeignKey(to='Unit', on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, to_field="url", on_delete=models.CASCADE)
    
    def __str__(self):  
        return self.title


class Unit(models.Model):
    title = models.CharField(max_length=128, unique=True)
    short = models.CharField(max_length=4, unique=True)
    
    def __str__(self):
        return self.title
		
class Tip(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200, unique=True)
    url_chosen = models.BooleanField(default=False)
    instructions = models.TextField()
    
    date_created = models.DateField(auto_now_add=True)
    public = models.BooleanField(default=False)
    
    objects = models.Manager()
	
    def save(self, *args, **kwargs):    
        if not self.url_chosen:
            url_variant = slugify(self.title + " " + str(datetime.now().date()))
            
            # avoid url collisions by appending an int if the url exists already
            same_urls = Recipe.objects.filter(url__contains=url_variant)
            if len(same_urls) > 0:
                url_variant = "{}-{}".format(url_variant, len(same_urls))
                
            self.url = url_variant
            self.url_chosen = True
            
        super(Tip, self).save(*args, **kwargs)
	
    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Recipe, on_delete=models.CASCADE)
