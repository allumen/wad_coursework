from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    return HttpResponse("index")

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
    
def register(request):
    pass
    
def login(request):
    pass

@login_required    
def logout(request):
    pass