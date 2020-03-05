import json

from .models          import Brand
from product.models   import Product

from django.views     import View
from django.http      import JsonResponse, HttpResponse
from django.db.models import Count, Q

class BrandListView(View):
    def get(self, request):
        return JsonResponse({"brand list": list(Brand.objects.values())}, status = 200)

class SearchProductView(View):
    def get(self, request):
        query = request.GET.get('query', None)
        searched_list = Product.objects.filter(Q(name__icontains = query) | Q(brand__name__icontains = query)).all()
        product_list = [
            {
                "product_image_url" : product.image_url,
                "brand_name"        : product.brand.name,
                "name"              : product.name,
                "price"             : product.price,
                "discounted_price"  : product.discounted_price,
            } for product in searched_list]
        return JsonResponse({"product_list": product_list}, status = 200)

class PopularBrandView(View):
    def get(self, request):
        ordered_brand_list = Brand.objects.prefetch_related('product_set')\
                             .annotate(product_count = Count('product')).order_by('-product_count').all()
        brand_list = [
            {
                'brand_id'        : brand.id,
                'name'            : brand.name,
                'large_image_url' : brand.large_image_url,
                'product_count'   : brand.product_set.count(),
            } for brand in ordered_brand_list[:30] ]
        return JsonResponse({"brand_list": brand_list}, status = 200)
