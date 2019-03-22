import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
django.setup()

from allgoorecipes.models import UserProfile, RecipeCategory, Recipe, Ingredient, Unit, Comment
from django.contrib.auth.models import User
from django.db import IntegrityError

def populate():
    print("Populating database...\n")

    username = 'admin'
    email = 'admin@email.com'
    password = 'password'

    baking = add_recipeCategory('Baking')
    cooking = add_recipeCategory('Cooking')
    drink = add_recipeCategory('Drink')
    tips = add_recipeCategory('Tips')

    add_recipe('Brownie',

    create_superUser(username, email, password)
    def add_recipeCategory(name):
        g, created = RecipeCategory.object.get_or_create(name = name)
        return g

    def add_recipe():
        m,created = Recipe.objects.get_or_create()
        m.recipeCategory.add(*category)
        return m

    def create_super_user(username, email, password):
        try:
            u = UserProfile.objcts.create_superuser(username, email, password)
            return u
        except IntegrityError:
            pass        

if __name == "__main__":
    print("Starting allgoodrecipes...")
    populate()
