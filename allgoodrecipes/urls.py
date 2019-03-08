from django.urls import path
from allgoodrecipes import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', include([
        path('', views.profile, name='profile'),
        path('settings/', views.profile_settings),
        path('publications/', views.profile_publications),
        path('comments/', views.profile_comments),
    ])),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
	path('recipes/', views.recipes, name='recipes'),
	path('tips/', views.tips, name='tips'),
	
]