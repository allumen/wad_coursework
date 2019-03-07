from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    return HttpResponse("index")

@login_required
def profile(request):
    return HttpResponse("profile")

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