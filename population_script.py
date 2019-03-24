import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad_coursework.settings')
django.setup()

from allgoodrecipes.models import UserProfile, RecipeCategory, Recipe, Ingredient, Unit, Comment
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.files import File


def add_user(username, email, password, isSuperUser):
    if isSuperUser == True:
        django_user = User.objects.create_superuser(username=username, email=email, password=password)
        django_user.is_superuser = True
    else:
        print(password)
        django_user = User.objects.create(username=username, email=email, password=password)
    django_user.save()
    user = UserProfile.objects.create(user=django_user)
    user.save()
    return user
    
def add_unit(title, short):
    unit = Unit.objects.create(title=title, short=short)
    return unit

def add_recipeCategory(name):
    g, created = RecipeCategory.objects.get_or_create(title=name)
    return g

def add_recipe(title, description, preparation_time, servings_number, instructions, image, categories, user):
    print(user.user.username)
    g = Recipe.objects.create(title=title, description=description,
                 preparation_time=preparation_time, servings_number=servings_number, instructions=instructions,
                 user=user, public=True)
    g.categories.add(*categories)
    if image is not None:
        g.image.save(os.path.join(g.url, g.url + "jpg"), image, save=True)
    return g

def get_recipe_details_from_file(filename):
    name, extension = os.path.splitext(filename)
    print("n: " + name, "e: " + extension)
    description = ''
    preparation_time = ''
    servings_number = ''
    instructions = ''
    image = None
    try:
        image = File(open(os.path.join("population_content", name + ".jpg"), "rb"))
    except FileNotFoundError:
        pass
    
    with open(os.path.join("population_content", filename), "r") as f:
        line_counter = 0
        for line in f:
            if line_counter == 0:
                description = line
            elif line_counter == 1:
                preparation_time = line
            elif line_counter == 2:
                servings_number = line
            else:
                instructions += line + "<br>"
            line_counter += 1
    
    return (name, description, preparation_time, servings_number, instructions, image)
                
def populate():
    print("Populating database...\n")

    # create users
    admin = add_user('admin', 'admin@email.com', 'admin', True)
    cleo = add_user('Cleo', 'cleo@email.com', 'password1', False)
    tamara = add_user('Tamara', 'tamara@email.com', 'password1', False)
    sue = add_user('Sue', 'sue@email.com', 'password1', False)
    ellie = add_user('Ellie', 'ellie@email.com', 'password1', False)
    mel = add_user('Mel', 'mel@email.com', 'password1', False)
    karen = add_user('Karen', 'karen@email.com', 'password1', False)

    # create categories
    baking = add_recipeCategory('Baking')
    cooking = add_recipeCategory('Cooking')
    drink = add_recipeCategory('Drink')
    tips = add_recipeCategory('Tips')
    fish = add_recipeCategory('Fish')
    chicken = add_recipeCategory('Chicken')
    meat = add_recipeCategory('Meat')
    deserts = add_recipeCategory('Deserts')
    mains = add_recipeCategory('Main courses')
    
    # add untis
    add_unit("gram", "g")
    add_unit("cup", "cup")
    add_unit("tablespoon", "tbsp")
    add_unit("teaspoon", "tspn")
    add_unit("ounce", "oz")
    add_unit("millilitre", "ml")
    add_unit("unit", "unit")
    add_unit("piece", "pcs")
    
    # add recipes
    add_recipe(*get_recipe_details_from_file("Tres leches cake.txt"), categories=[baking, deserts], user=cleo)
    add_recipe(*get_recipe_details_from_file("Sticky cherry bakewell buns.txt"), categories=[baking, deserts], user=tamara)
    add_recipe(*get_recipe_details_from_file("Spiced carrot & lentil soup.txt"), categories=[mains], user=tamara)
    add_recipe(*get_recipe_details_from_file("Southern-fried quail with blue cheese dressing.txt"), categories=[chicken, cooking], user=cleo)
    add_recipe(*get_recipe_details_from_file("Creamy garlic, lemon & spinach salmon.txt"), categories=[mains, fish, cooking], user=sue)
    add_recipe(*get_recipe_details_from_file("Classic meatloaf with tomato sauce.txt"), categories=[mains, meat, cooking, baking], user=karen)
    add_recipe(*get_recipe_details_from_file("Braised lamb & goat's cheese pies with gravy.txt"), categories=[meat, mains], user=mel)


if __name__ == "__main__":
    print("Starting allgoodrecipes...")
    populate()
