import json

from .models import Brand, Product, Color, ProductColor

from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

class BrandListView(View):
    def get(self, request):
        return JsonResponse({"brand list": list(Brand.objects.values())}, status = 200)

class ProductColorView(View):
    def get(self, request, product_id):
        try:
            product_color_list = ProductColor.objects.filter(product_id = product_id).select_related('color').all()
            color_list = [product_color.color.name for product_color in product_color_list]
            return JsonResponse({"color_list": color_list}, status = 200)
        except Product.DoesNotExist:
            return JsonResponse({"message": "INVALID_PRODUCT_ID"}, status = 400)
