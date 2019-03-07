from django.urls import path
from allgoodrecipes import views

urlpatterns = [
    path('', views.index, name='index'),
]
