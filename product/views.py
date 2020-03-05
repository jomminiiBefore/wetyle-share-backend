import json

from .models          import Brand, Product, ProductLike
from user.models      import User
from user.utils       import login_decorator

from django.views     import View
from django.http      import JsonResponse, HttpResponse
from django.db.models import Q

class BrandListView(View):
    def get(self, request):
        return JsonResponse({"brand list": list(Brand.objects.values())}, status = 200)

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
