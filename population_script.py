import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
django.setup()

from allgoorecipes.models import UserProfile, RecipeCategory, Recipe, Ingredient, Unit, Comment
from django.contrib.auth.models import User
from django.db import IntegrityError

def add_user(username, email, password, isSuperUser):
    user = UserProfile.objects.create_user(username, email, password)
    if superUser == True:
        user.is_superuser = True
    else:
        user.is_superuser = False
    user.save()

def add_recipeCategory(name):
    g, created = RecipeCategory.object.get_or_create(name = name)
    return g

def add_recipe(name):
    g, created = RecipeCategory.object.get_or_create(name = name)
    return g

def populate():
    print("Populating database...\n")

    # create users
    add_user('admin', 'admin@email.com', 'password', True)
    add_user('Cleo', 'cleo@email.com', 'password', False)
    add_user('Tamara', 'tamara@email.com', 'password', False)
    add_user('Sue', 'sue@email.com', 'password', False)
    add_user('Ellie', 'ellie@email.com', 'password', False)
    add_user('Mel', 'mel@email.com', 'password', False)
    add_user('Karen', 'karen@email.com', 'password', False)

    # create categories
    baking = add_recipeCategory('Baking')
    cooking = add_recipeCategory('Cooking')
    drink = add_recipeCategory('Drink')
    tips = add_recipeCategory('Tips')


if __name == "__main__":
    print("Starting allgoodrecipes...")
    populate()
