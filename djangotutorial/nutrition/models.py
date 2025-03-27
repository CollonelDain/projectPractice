from django.db import models
from django.contrib.auth.models import User

class FoodCategory(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, null=True)
    calories = models.PositiveIntegerField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    
    def __str__(self):
        return self.name

class Meal(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'),
        ('snack', 'Перекус'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=10, choices=MEAL_CHOICES)
    foods = models.ManyToManyField(Food, through='MealFood')
    date = models.DateField(auto_now_add=True)
    
    def total_calories(self):
        return sum(mf.calories for mf in self.mealfood_set.all())
    
    def __str__(self):
        return f"{self.get_meal_type_display()} ({self.date})"

class MealFood(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1)
    
    @property
    def calories(self):
        return self.food.calories * self.quantity
    
    def __str__(self):
        return f"{self.food.name} ({self.quantity} пор.)"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    daily_calorie_goal = models.PositiveIntegerField(default=2000)
    
    def __str__(self):
        return f"Профиль {self.user.username}"