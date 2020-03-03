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


""" 상세 이미지 데이터 모델 머지 후 코드 변경
class PopularityProductView(View):
    def get(self, request, product_id):
        try:
            product_likes = ProductLike.objects.filter(product_id = product_id)
            products = Product.objects.select_related('brand').all()          

            product_list = [{
                    'image_url'        : product.image_url,
                    'brand'            : product.brand,
                    'name'             : product.name,                    
                    'price'            : product.price,
                    'discounted_price' : product.discounted_price,                    
                    'product_like'     : [{
                        product_like.count()
                    } for product_like in product_likes],
                    
                    } for product in products]

            return JsonResponse({"products": product_list}, status = 200)
            
        except Product.DoesNotExist:
            return JsonResponse({"message": "NO_PRODUCT"}, status = 400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)

class PopularityBrandView(View):
    def get(self, request):
        try:
            brands = Brand.objects.all()
            brand_list = [{
                'name'               : brand.name,
                'small_image_url'    : brand.small_image_url
            } for brand in brands]
            return JsonResponse({"brand list": list(brand)}, status = 200)

        except Brand.DoesNotExist:
            return JsonResponse({"message": "NO_BRAND"}, status = 400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)


class PopularityKeyword(View):
    def get(self, request):
        try:
            keyword = SecondCategory.objects.filter(name).order_by('updeated_at')[:6]  
            if keyword.exitsts():
                return JsonResponse({"category_keyword_list": list(keyword)}, status = 200)
        
            products = Product.objects.select_related('brand').get(name=name).prefetch_related('product_like').get(id = id)        
            product_list = [{
                    'image_url'        : element.image_url,
                    'brand'            : element.brand.name,
                    'name'             : element.name,
                    'price'            : element.price,
                    'discounted_price' : element.discounted_price,
                    'point'            : element.point,
                    'detailed_info'    : element.detailed_info,
                    'add_info'         : element.add_info,
                    } for element in products]

            return JsonResponse({"products": product_list}, status = 200)
            

        except SecondCategory.DoesNotExist:
            return JsonResponse({"message": "NO_SECOND_CATEGORY"}, status = 400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)


class SearchView(View):
    def search(self, request):
        # name=value인 값을 가져옴 값이 없으면 ''으로 대체함
        value = request.GET.get('value', '')

        # 템플릿에 랜더링 될 변수를 모아놓을 딕셔너리 자료형
        render_args = {
            'value' : value,
        }

        # value의 값이 존재하는 경우
        if not value == '':
            # 포스트를 최신순으로 가져옴
            products = Product.objects.order_by('created_date').reverse()
            # 제목에 value가 포함되거나 작성자가 value인 포스트만 걸러냄
            products = products.filter(Q(name__icontains=value) | Q(author__name=value))
            render_args['products'] = products
        return render(request, render_args)


class RecommendView(View):
    def get(self, request):
        spaces = list(Spaces.objects.prefetch_related('tags_set').all())[:6]
        recommend = [{
            'title': space.title,
            'price': space.price,
            'location': space.location,
            'tag' : list(space.tags_set.values_list('tag', flat=True)),
            'image': list(space.images_set.filter(space_id=space.id).values('space_image'))
        } for space in spaces]

        return JsonResponse({'data': recommend}, status=200)

class ProductView(View):
    def get(self, request, product_id):

class SecondCategoryView(View):
    def get(self, request):
        second_categories = SecondCategory.values()
        return JsonResponse({"second_categories": list(second_categories)})

class ThirdCategoryView(View):
    def get(self, request):
        third_categories = ThirdCategory.values()
        return JsonResponse({"third_categories": list(third_categories)})
"""