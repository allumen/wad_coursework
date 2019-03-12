from django.urls import path, include
from allgoodrecipes import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_recipe', views.add_recipe, name='add_recipe'),
    path('profile/', include([
        path('', views.profile, name='profile'),
        path('settings/', views.profile_settings),
        path('publications/', views.profile_publications),
        path('comments/', views.profile_comments),
    ])),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
