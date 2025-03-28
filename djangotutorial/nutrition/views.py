from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import get_resolver, URLPattern, URLResolver
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os


from .models import Food, Meal, MealFood, UserProfile
from .serializers import *


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class MealFoodViewSet(viewsets.ModelViewSet):
    queryset = MealFood.objects.all()
    serializer_class = MealFoodSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


@api_view(['GET'])
def api_home(request):
    """
    Возвращает список всех доступных маршрутов API во всем проекте.
    """
    url_resolver = get_resolver()
    api_endpoints = collect_routes(url_resolver.url_patterns, request)

    return Response({
        'message': 'Список всех доступных маршрутов API',
        'routes': api_endpoints,
        'total': len(api_endpoints)
    })

def collect_routes(patterns, request, prefix=""):
    """
    Рекурсивно собирает все маршруты API во всем Django-проекте и корректно формирует URL.
    """
    routes = []
    base_url = get_base_url(request)  # Определяем базовый URL

    for pattern in patterns:
        if isinstance(pattern, URLPattern):  # Обычный маршрут (конкретный URL)
            route = f"{base_url}/{prefix}{pattern.pattern}"
            
            # Проверяем, содержит ли маршрут символ "<" (используется в регулярных выражениях)
            if "<" in route:
                continue  # Пропускаем этот маршрут
            
            route = route.replace("^", "").replace("$", "").replace("\\", "")  # Убираем спецсимволы
            routes.append({
                'url': route,
                'name': pattern.name or str(pattern.pattern)
            })
        elif isinstance(pattern, URLResolver):  # Вложенные маршруты (include)
            routes.extend(collect_routes(pattern.url_patterns, request, f"{prefix}{pattern.pattern}"))

    return routes


def get_base_url(request=None):
    """
    Возвращает базовый URL в зависимости от окружения
    """
    if 'CODESPACE_NAME' in os.environ:
        codespace_name = os.environ.get('CODESPACE_NAME')
        return f"https://{codespace_name}-8000.app.github.dev"
    else:
        return "http://localhost:8000"  # Фиксированный хост