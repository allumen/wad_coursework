from django.shortcuts import render
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from allgoodrecipes.forms import UserForm, UserProfileForm, RecipeForm
from allgoodrecipes.models import Recipe, RecipeCategory, UserProfile, Ingredient, Ingredient, Unit, Comment
from django.contrib.auth.models import User

import datetime
from calendar import timegm
from functools import wraps

from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.template.response import TemplateResponse
from django.utils.http import http_date

def index(request):
    recipes = category_list = Recipe.objects.order_by('-date_created')
    #tips
    return render(request, 'allgoodrecipes/index.html', context={'recipes':recipes})

def recipe_search(request, category_title=None):
    context_dict = {}

    if category_title:
        category = RecipeCategory.objects.get(title=category_title)
        context_dict['recipes'] = Recipe.objects.filter(categories__in=[category]).order_by('-date_created')
    else:
        context_dict['recipes'] = Recipe.objects.all()

    return render(request, 'allgoodrecipes/search.html', context=context_dict)
    
def search_ajax(request):
    search_target = request.POST.get('target')
    query = request.POST.get('query')
    response_data = {}
    
    if search_target == 'category':
        suggestions = RecipeCategory.objects.filter(title__contains=query)[:5]
        response_data['results'] = [s.title for s in suggestions]
        if response_data['results'] == []:
            response_data['results'] = ["Nothing found"]
        return JsonResponse(response_data)
        
    
def view_recipe(request, recipe_url):
    try:
        recipe = Recipe.objects.get(url=recipe_url)
        ingredients = Ingredient.objects.all()
        comments = Comment.objects.filter(post=recipe).order_by('-date')
        
        try:
            preparation_time = {1:"1-15 mins",
                                2:"15-30 mins",
                                3:"30-45 mins",
                              4:"45-60 mins",
                              5:"1-1.5 hrs",
                              6:"1.5-2 hrs",
                              7:"2-3 hrs",
                              8:"3-4 hrs",
                              9:"4+ hrs"}[recipe.preparation_time]
        except KeyError:
            preparation_time = "Corrupt value"
            
        return render(request, 'allgoodrecipes/view_recipe.html', context={'recipe': recipe, 'ingredients': ingredients, 'preparation_time': preparation_time, 'comments': comments})
    except Recipe.DoesNotExist:
        raise Http404
		
def view_tip(request, tip_url):
    try:
        tip = Tip.objects.get(url=tip_url)
		
        return render(request, 'allgoodrecipes/view_recipe.html', context={'recipe': recipe})
    except Tip.DoesNotExist:
        raise Http404
		
		
@login_required
def edit_recipe(request, recipe_url):
    response_data = {}
    
    try:
        action = request.GET.get('action')
        if action is None:
            action = request.POST.get('action')
        
        recipe = Recipe.objects.get(url=recipe_url)
            
        if action == "change_public":
            recipe.public = not recipe.public
            recipe.save()
            
            response_data["status"] = "success"
        elif action == "update_image":
            image = request.FILES.get('imageFile')
            if image is not None:
                recipe.image = image
                recipe.save()
                response_data["status"] = "success"
                response_data["image_url"] = recipe.image.name
            else:
                response_data["status"] = "fail"
        elif action == "add_category":
            category_name = request.POST.get('category_name')
            category = RecipeCategory.objects.get(title=category_name)
            recipe.categories.add(category)
            response_data["status"] = "success"
            response_data["category_title"] = category.title
        elif action == "remove_category":
            category_name = request.POST.get('category_name')
            category = RecipeCategory.objects.get(title=category_name)
            recipe.categories.remove(category)
            response_data["status"] = "success"
            response_data["category_title"] = category.title
        else:
            response_data["status"] = "fail"
            response_data["error"] = "Incorrect ajax, action undefined"
        return JsonResponse(response_data)
        
    except Recipe.DoesNotExist:
        response_data["status"] = "fail"
        response_data["error"] = "Recipe does not exist"
        return JsonResponse(response_data)
    except RecipeCategory.DoesNotExist:
        response_data["status"] = "fail"
        response_data["error"] = "Category does not exist"
        return JsonResponse(response_data)
    
@login_required
def add_recipe(request):
    add_successful = False
    IngredientsFormSet = inlineformset_factory(Recipe, Ingredient, exclude=("delete",), can_delete=False, extra=20, # extra specifies number of forms in set to render by default
                                               min_num=1, validate_min=True, max_num=20, validate_max=True)
    context_dict = {}
    
    # details submitted, try to add a new recipe
    if request.method == 'POST':
        # get recipe details
        recipe_form = RecipeForm(request.POST, request.FILES)
        
        if recipe_form.is_valid():     
            # delay saving of new recipe object
            recipe = recipe_form.save(commit=False)  
            # add rest of the fields
            recipe.user = UserProfile.objects.get(user=request.user)
            recipe.save()
            
            ingredients_form = IngredientsFormSet(data=request.POST, instance=recipe)
            add_successful = True
            
            if ingredients_form.is_valid():
                ingredients_form.save()
                context_dict = {'add_successful':add_successful,
                            'ingredients_set_form': ingredients_form,
                            'recipe_url': recipe.url}
                # Success!
                return render(request, 'allgoodrecipes/add_recipe.html', context=context_dict)
            # ingredients invalid, fallback to default page render
            else:
                context_dict['error_message'] = ingredients_form.errors + ingredients_form.non_form_errors()
        # recipe details invalid, fallback to default page render
        else:
            context_dict['error_message'] = recipe_form.errors
    
    # default page load
    recipe_form = RecipeForm()
    ingredients_set_form = IngredientsFormSet()
   
    context_dict['unit_choices'] = Unit.objects.all()
    context_dict['recipe_form'] = recipe_form
    context_dict['add_successful'] = add_successful
    context_dict['ingredients_set_form'] = ingredients_set_form

    return render(request, 'allgoodrecipes/add_recipe.html', context=context_dict)
        

@login_required
def profile(request):
    context_dict = {}
    return render(request, 'allgoodrecipes/profile.html', context=context_dict)

@login_required
def profile_settings(request):
    pass

@login_required
def profile_publications(request):
    pass

@login_required
def profile_comments(request):
    pass
    
def privacy(request):
    pass
    
def terms(request):
    pass
    
def contact(request):
    return render(request, 'allgoodrecipes/contact.html', {})
    
def register(request):
    # tell the template if registration successful
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            
            user.set_password(user.password)
            user.save()
            
            # commit = False to delay saving the model until we can avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            
            # tell template registration is successfull
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
            return render(request, 'allgoodrecipes/register.html', context={'error_message': "Registration unsucsessful!"})
    else:
        # not a POST request render registration form with blank ModelForm instances
        user_form = UserForm()
        profile_form = UserProfileForm()        

    context_dict = {'user_form': user_form,
                    'profile_form': profile_form,
                    'registration_complete': registered}
                      
    return render(request, 'allgoodrecipes/register.html', context=context_dict)
    
# *user_login* is used instead of *login* as the latter would shadow django.auth.login() function
def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('profile'))
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # if a user object returned, combaination valid
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                # Login SUCCESSFUL
                next_page = request.POST.get('redirect_url')
                if next_page:
                    return HttpResponseRedirect(next_page)
                else:
                    return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Your account is disabled')
        else:
            error_message = ''
            
            try:
                user = User.objects.get(username=username)
                print("Invalid password for user {}: {}".format(username, password))
                error_message = "Invalid password for user {}".format(username)
            except User.DoesNotExist:
                error_message = "User not found: {}".format(username)
                
            return render(request, 'allgoodrecipes/login.html', {'error_message': error_message})
    else:
        next_page = ''
        try:
            next_page = request.GET['next']
        except KeyError:
            pass
        return render(request, 'allgoodrecipes/login.html', {'redirect_url':next_page})

@login_required    
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
    
@login_required
def add_comment(request):
    try:
        url = request.POST.get('post_url')
        post = Recipe.objects.get(url=url)
        text = request.POST.get('comment_text')
        user = UserProfile.objects.get(user=request.user)
        if text is None or text == "" or text.isspace() or len(text.strip()) < 10:
            raise ValueError
        
        comment = Comment(
          user = user,
          text = text,
          post = post,
          )
        comment.save()
        
        return JsonResponse({"status": "success",
                             "new_comment_user": user.user.username,
                             "new_comment_date": comment.date.strftime("%B-%d, %Y, %I:%M%p")})
    except Recipe.DoesNotExist:
        return JsonResponse({"status": "fail",
                             "error": "postNotFound"})
    except ValueError:
        return JsonResponse({"status": "fail",
                             "error": "commentTextEmpty or too short (less than 10 chars)"})
