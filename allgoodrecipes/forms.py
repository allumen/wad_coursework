from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from allgoodrecipes.models import UserProfile, Recipe
           
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
        

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'description', 'instructions', 'preparation_time', 'servings_number', 'image')        
