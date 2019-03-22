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
    recipes = Recipe.objects.order_by('-date_created')
    categories = RecipeCategory.objects.all()
    recipes = category_list = Recipe.objects.order_by('-date_created')
    if Recipe.date_created == datetime.now().date():
        recipes2 = category_list = Recipe.objects.order_by('-date_created')[:3]
    #tips
    return render(request, 'allgoodrecipes/index.html', context={'recipes':recipes, 'recipes2':recipes2})

    
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
    
def x_robots_tag(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        response['X-Robots-Tag'] = 'noindex, noodp, noarchive'
        return response
    return inner


@x_robots_tag
def index(request, sitemaps,
          template_name='sitemap_index.xml', content_type='application/xml',
          sitemap_url_name='django.contrib.sitemaps.views.sitemap'):

    req_protocol = request.scheme
    req_site = get_current_site(request)

    sites = []  # all sections' sitemap URLs
    for section, site in sitemaps.items():
        # For each section label, add links of all pages of its sitemap
        # (usually generated by the `sitemap` view).
        if callable(site):
            site = site()
        protocol = req_protocol if site.protocol is None else site.protocol
        sitemap_url = reverse(sitemap_url_name, kwargs={'section': section})
        absolute_url = '%s://%s%s' % (protocol, req_site.domain, sitemap_url)
        sites.append(absolute_url)
        # Add links to all pages of the sitemap.
        for page in range(2, site.paginator.num_pages + 1):
            sites.append('%s?p=%s' % (absolute_url, page))

    return TemplateResponse(request, template_name, {'sitemaps': sites},
                            content_type=content_type)


@x_robots_tag
def sitemap(request, sitemaps, section=None,
            template_name='sitemap.xml', content_type='application/xml'):

    req_protocol = request.scheme
    req_site = get_current_site(request)

    if section is not None:
        if section not in sitemaps:
            raise Http404("No sitemap available for section: %r" % section)
        maps = [sitemaps[section]]
    else:
        maps = sitemaps.values()
    page = request.GET.get("p", 1)

    lastmod = None
    all_sites_lastmod = True
    urls = []
    for site in maps:
        try:
            if callable(site):
                site = site()
            urls.extend(site.get_urls(page=page, site=req_site,
                                      protocol=req_protocol))
            if all_sites_lastmod:
                site_lastmod = getattr(site, 'latest_lastmod', None)
                if site_lastmod is not None:
                    site_lastmod = (
                        site_lastmod.utctimetuple() if isinstance(site_lastmod, datetime.datetime)
                        else site_lastmod.timetuple()
                    )
                    lastmod = site_lastmod if lastmod is None else max(lastmod, site_lastmod)
                else:
                    all_sites_lastmod = False
        except EmptyPage:
            raise Http404("Page %s empty" % page)
        except PageNotAnInteger:
            raise Http404("No page '%s'" % page)
    response = TemplateResponse(request, template_name, {'urlset': urls},
                                content_type=content_type)
    if all_sites_lastmod and lastmod is not None:
        # if lastmod is defined for all sites, set header so as
        # ConditionalGetMiddleware is able to send 304 NOT MODIFIED
        response['Last-Modified'] = http_date(timegm(lastmod))
    return response   
    
    
def contact(request):
    return HttpResponseRedirect('contact/')
    
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
