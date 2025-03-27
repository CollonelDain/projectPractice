from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Food, Meal, MealFood, UserProfile
from .forms import FoodForm, MealForm, MealFoodForm, UserRegisterForm, UserProfileForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Создаем профиль для нового пользователя
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'nutrition/register.html', {'form': form})

@login_required
def dashboard(request):
    meals = Meal.objects.filter(user=request.user).order_by('-date')[:7]
    profile = UserProfile.objects.get(user=request.user)
    
    # Расчет суммарных показателей за сегодня
    today_meals = meals.filter(date=timezone.now().date())
    total_calories = sum(meal.total_calories() for meal in today_meals)
    
    return render(request, 'nutrition/dashboard.html', {
        'meals': meals,
        'profile': profile,
        'total_calories': total_calories,
    })

@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'nutrition/profile.html', {'form': form})


@login_required
def add_food(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('food_list')
    else:
        form = FoodForm()
    return render(request, 'nutrition/food_form.html', {'form': form})

@login_required
def food_list(request):
    foods = Food.objects.all()
    return render(request, 'nutrition/food_list.html', {'foods': foods})

@login_required
def add_meal(request):
    if request.method == 'POST':
        meal_form = MealForm(request.POST)
        meal_food_form = MealFoodForm(request.POST)
        
        if meal_form.is_valid() and meal_food_form.is_valid():
            meal = meal_form.save(commit=False)
            meal.user = request.user
            meal.save()
            
            meal_food = meal_food_form.save(commit=False)
            meal_food.meal = meal
            meal_food.save()
            
            return redirect('dashboard')
    else:
        meal_form = MealForm()
        meal_food_form = MealFoodForm()
    
    return render(request, 'nutrition/meal_form.html', {
        'meal_form': meal_form,
        'meal_food_form': meal_food_form
    })