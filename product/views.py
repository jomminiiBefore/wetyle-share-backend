import json
import csv

from .models import Brand

from django.views import View
from django.http import JsonResponse, HttpResponse

class BrandListView(View):
    def get(self, request):
        result = []

        with open('../crawler/brand_infos.csv', mode='r') as brand_infos:
            reader = csv.reader(brand_infos)

            for list in reader:
                result.append(list)
        return JsonResponse({"brand list": result}, status = 200)

