"""
URL configuration for foodtracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from nutrition import views as nutrition_views
from rest_framework import routers
from nutrition import views_api
from rest_framework.authtoken.views import obtain_auth_token
from nutrition.nocodb_utils import get_nocodb_data


router = routers.DefaultRouter()
router.register(r'api/foods', views_api.FoodViewSet, basename='food')
router.register(r'api/meals', views_api.MealViewSet, basename='meal')
router.register(r'api/profile', views_api.UserProfileViewSet, basename='profile')


urlpatterns = [
    path('', api_home, name='api-home')
    path('admin/', admin.site.urls),
    path('register/', nutrition_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='nutrition/login.html'), name='login'),
#    path('logout/', auth_views.LogoutView.as_view(template_name='nutrition/logout.html'), name='logout'),
#    path('profile/', nutrition_views.profile, name='profile'),
    path('', nutrition_views.dashboard, name='dashboard'),
#    path('foods/', nutrition_views.food_list, name='food_list'),
#    path('foods/add/', nutrition_views.add_food, name='add_food'),
#    path('meals/add/', nutrition_views.add_meal, name='add_meal'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('nocodb-data/', get_nocodb_data, name='nocodb_data'),
]