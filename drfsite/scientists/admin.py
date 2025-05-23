from django.contrib import admin

from .models import Scientists, Food

# Register your models here.
admin.site.register(Scientists)
admin.site.register(Food)