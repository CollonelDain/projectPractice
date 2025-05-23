from django.urls import path
from .views import FoodListView
from . import views

urlpatterns = [
    path("", FoodListView.as_view(), name="food_list"),
]