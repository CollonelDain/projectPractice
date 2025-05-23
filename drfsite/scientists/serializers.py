from rest_framework import serializers
from .models import Scientists, Food


class ScientistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scientists
        fields = ('title', 'cat_id')


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('name', 'caloties', 'protein', 'carbs', 'fats')
