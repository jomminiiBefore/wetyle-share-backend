import jwt
import json
import requests

from user.models              import User
from card.models              import Style, StyleLike, StyleRelatedItem, StyleComment
from user.utils               import login_decorator
from .style_related_item_data import random_item

from django.views             import View
from django.http              import JsonResponse, HttpResponse
from django.core.exceptions   import ObjectDoesNotExist

class StyleView(View):
    def get(self, request, style_id):
        try:
            request_style = Style.objects.get(id = style_id)
            style_user    = Style.objects.select_related('user').get(id = style_id).user
            comments       = Style.objects.prefetch_related('comments')\
                            .select_related('user').get(id = style_id).comments
            style = [
                {
                    'style_image_url'     : request_style.image_url,
                    'related_item'        : list(request_style.style_related_items.values()),
                    'description'         : request_style.description,
                    'profile_image_url'   : style_user.image_url,
                    'nickname'            : style_user.nickname,
                    'profile_description' : style_user.description,
                    'like_count'          : StyleLike.objects.filter(style_id = style_id).count(),
                    'comment_count'       : comments.all().count(),
                    'comment'             : [
                        {
                            'profile_image' : comment.user.image_url,
                            'nickname'      : comment.user.nickname,
                            'description'   : comment.description,
                            'date'          : str(comment.updated_at)[2:11],
                            } for comment in comments.all()]
                    }]
            return JsonResponse({"result": style}, status = 200)
        except Style.DoesNotExist:
            return JsonResponse({"message": "INVALID_STYLE_ID"}, status = 400)

class DailyLookCardView(View):
    def get(self, request):
        style_list = Style.objects.all().prefetch_related('style_related_items', 'comments')
        card_list = [
            {
                'style_image_url'    : style.image_url,
                'related_item'       : list(style.style_related_items.values()),
                'profile_image_url'  : style.user.image_url,
                'nickname'           : style.user.nickname,
                'profile_description': style.user.description,
                'date'               : str(style.created_at)[2:11],
                'like_count'         : StyleLike.objects.filter(style_id = style.id).count(),
                'comment_count'      : style.comments.all().count(),
                # collection 사용 시 작성
                # 'collection_count': ,
                'comment'            : [
                    {
                        'profile_image' : comment.user.image_url,
                        'nickname'      : comment.user.nickname,
                        'description'   : comment.description,
                        'date'          : str(comment.updated_at)[2:11],
                        }
                    for comment in style.comments.all()],
            } for style in style_list]
        return JsonResponse({"card_list": card_list}, status = 200)

class StyleUploadView(View):
    @login_decorator
    def post(self,request):
        data = json.loads(request.body)
        try:
            make = Style.objects.create(
                description  = data['description'],
                image_url    = data['image_url'],
                user_id      = request.user.id
            )
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

        random_item_list = random_item()
        StyleRelatedItem(
            pants        = random_item_list['pants'],
            skirt        = random_item_list['skirt'],
            shoes        = random_item_list['shoes'],
            bag          = random_item_list['bag'],
            accessory    = random_item_list['accessory'],
            etc          = random_item_list['etc'],
            style_id     = make.id
        ).save()
        return HttpResponse(status = 200)


class StyleCommentUploadView(View):
    @login_decorator
    def post(self, request, style_id):
        data = json.loads(request.body)
        try:
            StyleComment(
                description = data['description'],
                style_id    = style_id,
                user_id     = request.user.id,
            ).save()
            return HttpResponse(status = 200)
        except Style.DoesNotExist:
            return JsonResponse({"message": "INVALID_STYLE_ID"}, status = 400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

class StyleCommentGetView(View):
    def get(self, request, style_id):
        try:
            style = Style.objects.prefetch_related('comments').get(id = style_id)
            comment_list = [
                {
                    'comment_count' : style.comments.all().count(),
                    'comment' :[
                        {
                            'profile_image' : comment.user.image_url,
                            'nickname'      : comment.user.nickname,
                            'description'   : comment.description,
                            'date'          : str(comment.updated_at)[2:11],
                            } for comment in style.comments.all()]
                }]
            return JsonResponse({"comment": comment_list}, status = 200)
        except Style.DoesNotExist:
            return JsonResponse({"message": "INVALID_STYLE_ID"}, status = 400)
