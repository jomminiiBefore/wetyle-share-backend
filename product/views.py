import json

from .models          import Brand, Product, ProductLike, ProductColor, Color
from user.models      import User
from user.utils       import login_decorator

from django.views     import View
from django.http      import JsonResponse, HttpResponse
from django.db.models import Q, Count
from django.core.exceptions import ObjectDoesNotExist

class BrandListView(View):
    def get(self, request):
        return JsonResponse({"brand list": list(Brand.objects.values())}, status = 200)

class ProductColorView(View):
    def get(self, request, product_id):
        try:
            product_color_list = ProductColor.objects.filter(product_id = product_id).select_related('color').all()
            color_list = [{
                "color_id"  : product_color.color.id,
                "color_name": product_color.color.name
            } for product_color in product_color_list]
            return JsonResponse({"color_list": color_list}, status = 200)
        except Product.DoesNotExist:
            return JsonResponse({"message": "INVALID_PRODUCT_ID"}, status = 400)

class ProductLikeView(View):
    @login_decorator
    def get(self, request, product_id):
        try:
            if ProductLike.objects.filter(Q(user_id = request.user.id) & Q(product_id = product_id)).exists():
                ProductLike.objects.filter(Q(user_id = request.user.id) & Q(product_id = product_id)).delete()
                return HttpResponse(status = 200)
            Product.objects.get(id = product_id).product_like.add(User.objects.get(id = request.user.id))
            return HttpResponse(status = 200)
        except Product.DoesNotExist:
            return JsonResponse({"message": "INVALID_PRODUCT_ID"}, status = 400)

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
