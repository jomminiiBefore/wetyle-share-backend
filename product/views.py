import json
import jwt
import requests

from product.models         import (
    Product,
    Brand,
    ProductLike,
    ProductDetailImage,
    ProductSize,
    ProductInqury,
    ProductSize,
    Size,
    ProductColor,
    Color
)

from my_settings            import SECRET_KEY
from .models                import Brand, Product, ProductLike, ProductColor, Color
from card.models            import Style
from user.models            import User
from user.utils             import login_decorator

from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models       import Q, Count

class BrandListView(View):
    def get(self, request):
        return JsonResponse({"brand_list": list(Brand.objects.values())}, status = 200)

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
        product_list  = [{
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
        brand_list = [{
            'brand_id'        : brand.id,
            'name'            : brand.name,
            'large_image_url' : brand.large_image_url,
            'product_count'   : brand.product_set.count(),
            } for brand in ordered_brand_list[:30] ]
        return JsonResponse({"brand_list": brand_list}, status = 200)

class ProductView(View):
    def get(self, request, product_id):
        try:
            access_token = request.headers.get('Authorization', None)
            is_like      = None
            if access_token:
                payload  = jwt.decode(access_token, SECRET_KEY, algorithm = 'HS256')
                user     = User.objects.get(login_id = payload['login_id'])
                is_like  = ProductLike.objects.filter(Q(user_id = user.id) & Q(product_id = product_id)).exists()
            product_all = Product.objects.prefetch_related('productdetailimage_set', 'productlike_set').get(id = product_id)
            product = {
                'is_like'                : is_like,
                'product_id'             : product_all.id,
                'image_url'              : product_all.image_url,
                'name'                   : product_all.name,
                'discounted_price'       : product_all.discounted_price,
                'price'                  : product_all.price,
                'product_like'           : product_all.productlike_set.count(),
                'point'                  : product_all.point,
                'brand_name'             : product_all.brand.name,
                'brand_large_image_url'  : product_all.brand.large_image_url,
                'detail_image_url'       : [image['image_url'] for image in product_all.productdetailimage_set.all().values()]
                }
            return JsonResponse({"result": product}, status = 200)
        except Product.DoesNotExist:
            return JsonResponse({"message": "INVALID_PRODUCT_ID"}, status = 400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status = 400)

class PopularProductView(View):
    def get(self, request):
        try:
            ordered_product_list = Product.objects.prefetch_related('product_like')\
                                   .annotate(like_count = Count('product_like')).order_by('-like_count')[:36]
            product_list = [{
                'product_id'       : product.id,
                'image_url'        : product.image_url,
                'brand'            : product.brand.name,
                'name'             : product.name,
                'price'            : product.price,
                'discounted_price' : product.discounted_price,
                'product_like'     : product.product_like.count()
                } for product in ordered_product_list]
            return JsonResponse({"result": product_list[:36]}, status = 200)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)

class ProductSizeView(View):
    def get(self, request, product_id):
        try:
            product_size_list = ProductSize.objects.filter(product_id = product_id).select_related('size').all()
            size_list         = [{
                'size_id'          : size.size_id,
                'product_size'     : size.size.name
            } for size in product_size_list ]
            return JsonResponse({"size_list": size_list}, status = 200)
        except Product.DoesNotExist:
            return JsonResponse({"message": "INVALID_PRODUCT_ID"}, status = 400)
