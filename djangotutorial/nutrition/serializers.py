from rest_framework import serializers
from .models import Food, Meal, MealFood, UserProfile

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

class MealFoodSerializer(serializers.ModelSerializer):
    food = FoodSerializer()
    
    class Meta:
        model = MealFood
        fields = ['id', 'food', 'quantity', 'calories']

class MealSerializer(serializers.ModelSerializer):
    foods = MealFoodSerializer(source='mealfood_set', many=True)
    
    class Meta:
        model = Meal
        fields = ['id', 'user', 'meal_type', 'date', 'foods', 'total_calories']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['weight', 'height', 'daily_calorie_goal']