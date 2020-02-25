import json
import csv

from .models import Brand

from django.views import View
from django.http import JsonResponse, HttpResponse

class BrandListView(View):
    def get(self, request):
        result = []
        
        for i in Brand.objects.values():
            result.append(i)

        return JsonResponse({"brand list": result}, status = 200)

