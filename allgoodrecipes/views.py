from django.shortcuts import render
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from allgoodrecipes.forms import UserForm, UserProfileForm, RecipeForm
from allgoodrecipes.models import Recipe, UserProfile, Ingredient, Ingredient
from django.contrib.auth.models import User

def index(request):
    recipes = category_list = Recipe.objects.order_by('-date_created')
    #tips
    return render(request, 'allgoodrecipes/index.html', context={'recipes':recipes})

    
def view_recipe(request, recipe_url):
    try:
        recipe = Recipe.objects.get(url=recipe_url)
        ingredients = Ingredient.objects.all()
        print(ingredients)
        return render(request, 'allgoodrecipes/view_recipe.html', context={'recipe': recipe, 'ingredients': ingredients})
    except Recipe.DoesNotExist:
        raise Http404
    
@login_required
def add_recipe(request):
    add_successful = False
    
    IngredientsFormSet = inlineformset_factory(Recipe, Ingredient, exclude=("delete",), can_delete=False, extra=10)
    
    # process first stage
    if request.method == 'POST':
        recipe_form = RecipeForm(data=request.POST)
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
            else:
                context_dict = {
                            'error_message': ingredients_form.errors}
                return render(request, 'allgoodrecipes/add_recipe.html', context=context_dict)
            
            context_dict = {
                            'ingredients_set_form': ingredients_form,
                            'recipe_url': recipe.url}
                      
            return render(request, 'allgoodrecipes/add_recipe.html', context=context_dict)
        else:
            print(recipe_form.errors)
            context_dict = {
                            'error_message': recipe_form.errors}
            return render(request, 'allgoodrecipes/add_recipe.html', context=context_dict) 
    else:
        recipe_form = RecipeForm()
        ingredients_set_form = IngredientsFormSet()
        
        context_dict = {
                        'recipe_form': recipe_form,
                        'add_successful': add_successful,
                        'ingredients_set_form':ingredients_set_form}
                          
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
    
def map(request):
    pass
    
def contact(request):
    pass
    
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
def add_comment(request, pk):
  post = get_object_or_404(Post, pk=pk)
  comment = comment(
      user = UserProfile.objects.get(request.user),
      text = request.POST['comment'],
      post = Post.objects.get(request.title),
      )
  comment.save()
  return HttpResponseRedirect(reverse('allgoodrecipes.view_recipe'))
