import json
import requests
from user.models               import User
from product.models            import Product, Brand, ProductLike, ProductDetailImage

from django.views              import View
from django.http               import JsonResponse, HttpResponse
from django.core.exceptions    import ObjectDoesNotExist
from django.db.models          import Count

class BrandListView(View):
    def get(self, request):
        return JsonResponse({"brand list": list(Brand.objects.values())}, status = 200)


class ProductListView(View):
    def get(self, request, product_id):
        try:
            product_likes         = ProductLike.objects.filter(product_id = product_id)
            product_detail_images = ProductDetailImage.objects.filter(product_id = product_id)
            products              = Product.objects.select_related('brand').all()          

            product_list = [{                    
                    'name'                  : product.name,                    
                    'price'                 : product.price,
                    'discounted_price'      : product.discounted_price,
                    'detailed_info'         : product.detailed_info,
                    'add_info'              : product.add_info,
                    'brand_name'            : product.brand.name,
                    'brand_id'              : product.brand.id,
                    'brand_small_image_url' : product.brand.small_image_url,
                    'brand_large_image_url' : product.brand.large_image_url,
                    'brand_description'     : product.brand.description,
                    'product_like'     : [{
                        product_like.count()
                    } for product_like in product_likes],
                    'product_detail_image'  : [{
                        product_detail_image.image_url
                    } for product_detail_image in product_detail_images],                    
                    } for product in products]

            return JsonResponse({"products": product_list}, status = 200)

        except Product.DoesNotExist:
            return JsonResponse({"message": "NO_PRODUCT"}, status = 400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)           


