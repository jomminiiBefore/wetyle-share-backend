import json
import requests
from user.models               import User
from product.models            import Product, Brand, ProductLike, ProductDetailImage, ProductSize, ProductInqury, ProductSize, Size

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
            product_all = Product.objects.prefetch_related('productdetailimage_set', 'productlike_set').get(id = product_id)
            product = {
                  'product_id'             : product_all.id,
                  'image_url'              : product_all.image_url,
                  'name'                   : product_all.name,
                  'discounted_price'       : product_all.discounted_price,
                  'price'                  : product_all.price,
                  'product_like'           : product_all.productlike_set.count(),
                  'point'                  : product_all.point,
                  'brand_name'             : product_all.brand.name,
                  'brand_large_image_url'  : product_all.brand.large_image_url,
                  'detail_image_url'       : [ image['image_url'] for image in product_all.productdetailimage_set.all().values() ]
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
                    'brand'            : product.brand.name if not product.brand else ,                    
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

            size_list         = [{
                'size_id'          : size.size_id,
                'product_size'     : size.size.name
            } for size in product_size_list ]
            
            return JsonResponse({"size_list": size_list}, status = 200)
        except Product.DoesNotExist:
            return JsonResponse({"message": "INVALID_PRODUCT_ID"}, status = 400)
