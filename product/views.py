import json

from .models          import Brand
from product.models   import Product

from django.views     import View
from django.http      import JsonResponse, HttpResponse
from django.db.models import Count, Q

class BrandListView(View):
    def get(self, request):
        return JsonResponse({"brand list": list(Brand.objects.values())}, status = 200)

class PopularBrandView(View):
    def get(self, request):
        ordered_brand_list = Brand.objects.prefetch_related('product_set')\
                             .annotate(product_count = Count('product')).order_by('-product_count').all()
        brand_list = [
            {
                'brand_id'        : brand.id ,
                'name'            : brand.name ,
                'large_image_url' : brand.large_image_url ,
                'product_count'   : brand.product_set.count(),
            } for brand in ordered_brand_list[:30] ]
        return JsonResponse({"brand_list": brand_list}, status = 200)
