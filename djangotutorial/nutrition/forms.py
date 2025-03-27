from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Food, Meal, MealFood, UserProfile

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'category', 'calories', 'protein', 'carbs', 'fats']

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['meal_type']

class MealFoodForm(forms.ModelForm):
    class Meta:
        model = MealFood
        fields = ['food', 'quantity']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['weight', 'height', 'daily_calorie_goal']