from django.urls import path, include
from allgoodrecipes import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<recipe_url>/', views.view_recipe, name='view_recipe'),
    path('recipe/<recipe_url>/edit/', views.edit_recipe, name='edit_recipe'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('profile/', include([
        path('', views.profile, name='profile'),
        path('settings/', views.profile_settings, name= 'settings'),
        path('publications/', views.profile_publications),
        path('comments/', views.profile_comments),
    ])),
    path('search_ajax/', views.search_ajax, name='search_ajax'),
    path('add_comment/', views.add_comment, name = 'add_comment'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('privacy/', views.privacy, name='pp'),
    path('terms/', views.terms, name='tc'),
    path('map/', views.map, name='map'),
    path('contact/', views.contact, name='contact'),
]
