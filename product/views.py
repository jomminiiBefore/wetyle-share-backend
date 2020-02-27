import json

from .models import Brand

from django.views import View
from django.http import JsonResponse, HttpResponse

class BrandListView(View):
    def get(self, request):
        return JsonResponse({"brand list": list(Brand.objects.values())}, status = 200)

