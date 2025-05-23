from django.forms import model_to_dict
from rest_framework import generics
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import TemplateView

from .models import Scientists
from .serializers import ScientistsSerializer
from .nocodb import get_food


class ScientistsAPIView(APIView):
    def get(self, request):
        lst = Scientists.objects.all().values()
        return Response({'posts': list(lst)})

'''
    def post(self, request):
        post_new = Scientists.objects.create(
            title=request.data['title']
            content=request.data['content']
            cat_id=request.data['cat_id']
        )
        return Response({'post': model_to_dict(post_new)})
'''

class FoodListView(TemplateView):
    template_name = 'app/food_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table_id = 'mibm6agaouy0jey'  
        try:
            records = get_food(table_id)
            print(records)
        except Exception as e:
            records = []
            print(e)
        
        context['records'] = records
        return context




#class ScientistsAPIView(generics.ListAPIView):
#    queryset = Scientists.objects.all()
#    serializer_class = ScientistsSerializer