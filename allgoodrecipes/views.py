from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    return HttpResponse("index")

def profile(request):
    return HttpResponse("profile")
