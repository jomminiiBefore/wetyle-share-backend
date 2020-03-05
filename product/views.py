import json
import requests
from user.models               import User
from product.models            import Product, Brand, ProductLike, ProductDetailImage, ProductColor, ProductSize, ProductInqury, ProductSize, Size

from django.views              import View
from django.http               import JsonResponse, HttpResponse
from django.core.exceptions    import ObjectDoesNotExist
from django.db.models          import Q, Count

class BrandListView(View):
    def get(self, request):
        return JsonResponse({"brand list": list(Brand.objects.values())}, status = 200)

class ProductView(View):
    def get(self, request, product_id):
        try:
            product_obj           = Product.objects.select_related('brand').get(id = product_id)                 
            product_detail_image  = ProductDetailImage.objects.filter(product_id = product_id)            
            like_count            = ProductLike.objects.filter(product_id = product_id).count()            

            product = {
                'image_url'             : product_obj.image_url,
                'name'                  : product_obj.name,
                'discounted_price'      : product_obj.discounted_price,
                'price'                 : product_obj.price,                
                'product_like'          : like_count,
                'point'                 : product_obj.point,
                'brand_name'            : product_obj.brand.name,
                'brand_large_image_url' : product_obj.brand.large_image_url,                
                'detail_image_url'      : [image.image_url for image in product_detail_image],  
                'add_info'              : product_obj.add_info                
            }         
            return JsonResponse({"result": product}, status = 200)        

        except Product.DoesNotExist:
            return JsonResponse({"message": "INVALID_PRODUCT_ID"}, status = 400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)
           

class PopularProductView(View):
    def get(self, request, product_id):
        try:
            ordered_product_list = Product.objects.prefetch_related('product_like').annotate(like_count = Count('product_like')).order_by('-like_count')
            
            product_list = [
                {
                    'product_id'       : product.id,
                    'image_url'        : product.image_url,
                    'brand'            : product.brand.name,
                    'name'             : product.name,                    
                    'price'            : product.price,
                    'discounted_price' : product.discounted_price,                    
                    'product_like'     : ProductLike.objects.filter(product_id = product_id).count()                    
                    } for product in ordered_product_list ]
                    
            return JsonResponse({"result": product_list[:32]}, status = 200)
            
        except Product.DoesNotExist:
            return JsonResponse({"message": "INVALID_PRODUCT_ID"}, status = 400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)

class ProductSizeView(View):
    def get(self, request, product_id):
        try:
            product_size_list = ProductSize.objects.filter(product_id = product_id).select_related('size').all()
            size_list         = [product_size.size.name for product_size in product_size_list]
            return JsonResponse({"size_list": size_list}, status = 200)
        except Product.DoesNotExist:
            return JsonResponse({"message": "INVALID_PRODUCT_ID"}, status = 400)