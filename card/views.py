import jwt
import json
import requests

from user.models              import User
from card.models              import (
    Style,
    StyleLike,
    StyleRelatedItem,
    StyleComment,
    StyleImage,
    Collection,
    CollectionStyle,
    CollectionFollower
)
from user.utils               import login_decorator
from .style_related_item_data import random_item

from django.views             import View
from django.http              import JsonResponse, HttpResponse
from django.core.exceptions   import ObjectDoesNotExist
from django.db.models         import Q, Count

class StyleView(View):
    def get(self, request, style_id):
        try:
            style_obj    = Style.objects.get(id=style_id)
            style_comments = Style.objects.prefetch_related('comments').get(id=style_id).comments.all()
            styles    = Style.objects.prefetch_related('styleimage_set').get(id=style_id).styleimage_set.all()
            related_items = Style.objects.prefetch_related('style_related_items').get(id=style_id).style_related_items.all()
            like_count = StyleLike.objects.filter(style_id = style_id).count()

            style = {
                'style_image_url'     : [ style.image_url for style in styles],
                'related_item'        : list(related_items.values()),
                'description'         : style_obj.description,
                'profile_image_url'   : style_obj.user.image_url,
                'nickname'            : style_obj.user.nickname,
                'profile_description' : style_obj.user.description,
                'like_count'          : like_count,
                'comment_count'       : style_comments.count(),
                'comment'             : [
                    {
                        'profile_image' : comment.user.image_url,
                        'nickname'      : comment.user.nickname,
                        'description'   : comment.user.description,
                        'date'          : str(comment.user.updated_at)[2:11],
                    } for comment in style_comments]
            }
            return JsonResponse({"result": style}, status = 200)
        except Style.DoesNotExist:
            return JsonResponse({"message": "INVALID_STYLE_ID"}, status = 400)

class DailyLookCardView(View):
    def get(self, request):
        style_list = Style.objects.all().prefetch_related('style_related_items', 'comments')
        card_list = [
            {
                'style_id'           : style.id,
                'style_image_url'    : style.image_url,
                'related_item'       : list(style.style_related_items.values()),
                'profile_image_url'  : style.user.image_url,
                'nickname'           : style.user.nickname,
                'profile_description': style.user.description,
                'date'               : str(style.created_at)[2:11],
                'like_count'         : StyleLike.objects.filter(style_id = style.id).count(),
                'comment_count'      : style.comments.all().count(),
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
                user_id      = request.user.id
            )

            StyleImage.objects.create(
                image_url = data['image_url'],
                style_id = make.id
            )

            StyleRelatedItem.objects.create(
                pants        = random_item_list['pants'],
                skirt        = random_item_list['skirt'],
                shoes        = random_item_list['shoes'],
                bag          = random_item_list['bag'],
                accessory    = random_item_list['accessory'],
                etc          = random_item_list['etc'],
                style_id     = make.id
            )
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

class StyleCommentView(View):
    @login_decorator
    def post(self, request, style_id):
        data = json.loads(request.body)
        try:
            StyleComment.objects.create(
                description = data['description'],
                style_id    = style_id,
                user_id     = request.user.id,
            )
            return HttpResponse(status = 200)
        except Style.DoesNotExist:
            return JsonResponse({"message": "INVALID_STYLE_ID"}, status = 400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

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

class StyleLikeView(View):
    @login_decorator
    def get(self, request, style_id):
        try:
            click_user_id = request.user.id
            style_id      = Style.objects.get(id=style_id).id
            if StyleLike.objects.filter(Q(user_id = click_user_id) & Q(style_id = style_id)).exists():
                StyleLike.objects.filter(Q(user_id = click_user_id) & Q(style_id = style_id)).delete()
                return HttpResponse(status = 200)
            
            Style.objects.get(id = style_id).style_like.add(User.objects.get(id = click_user_id))
            return HttpResponse(status = 200)
        except Style.DoesNotExist:
            return JsonResponse({"message": "INVALID_STYLE_ID"}, status = 400)

class PopularCardView(View):
    def get(self, request):
        ordered_style_list = Style.objects.prefetch_related('style_like')\
                            .annotate(like_count = Count('style_like'))\
                            .order_by('-like_count')
        card_list = [
            {
                'style_id'           : style.id, 
                'style_image_url'    : style.image_url,
                'related_item'       : list(style.style_related_items.values()),
                'profile_image_url'  : style.user.image_url,
                'nickname'           : style.user.nickname,
                'profile_description': style.user.description,
                'date'               : str(style.created_at)[2:11],
                'like_count'         : StyleLike.objects.filter(style_id = style.id).count(),
                'comment_count'      : style.comments.all().count(),
                'comment'            : [
                    {
                        'profile_image' : comment.user.image_url,
                        'nickname'      : comment.user.nickname,
                        'description'   : comment.description,
                        'date'          : str(comment.updated_at)[2:11],
                    }
                    for comment in style.comments.all()],
            } for style in ordered_style_list]
        return JsonResponse({"card_list": card_list}, status = 200)

class CollectionView(View):
    def get(self, request, collection_id):
        try:
            collection_style_list = CollectionStyle.objects.filter(collection_id = collection_id).all()
            style_list = [ Style.objects.prefetch_related('style_related_items',
                'comments').get(id = collection_style.style_id) \
            for collection_style in collection_style_list]

            card_list  = [
                {
                    'style_id'           : style.id,
                    'style_image_url'    : list(style.styleimage_set.values()),
                    'related_item'       : list(style.style_related_items.values()),
                    'profile_image_url'  : style.user.image_url,
                    'nickname'           : style.user.nickname,
                    'profile_description': style.user.description,
                    'date'               : str(style.created_at)[2:11],
                    'like_count'         : StyleLike.objects.filter(style_id = style.id).count(),
                    'comment_count'      : style.comments.all().count(),
                    'collection_count'   : CollectionStyle.objects.filter(style_id = style.id).count() ,
                    'comment'            : [
                        {
                            'profile_image' : comment.user.image_url,
                            'nickname'      : comment.user.nickname,
                            'description'   : comment.description,
                            'date'          : str(comment.updated_at)[2:11],
                            }
                        for comment in style.comments.all()],
                } for style in style_list]

            collection      = Collection.objects.get(id = collection_id)
            collection_info = {
                'collection_id'   : collection.id,
                'image_url'       : collection.image_url,
                'name'            : collection.name,
                'description'     : collection.description,
                'follower_count'  : CollectionFollower.objects.filter(collection_id = collection_id).count(),
                'style_count'     : CollectionStyle.objects.filter(collection_id = collection_id).count(),
                'user'            : 
                {
                    'nickname'    : collection.user.nickname,
                    'login_id'    : collection.user.login_id,
                    'description' : collection.user.description,
                },
                'card_list'       : card_list,
            }
            return JsonResponse({"result": collection_info}, status = 200)
        except Collection.DoesNotExist:
            return JsonResponse({"message": "INVALID_COLLECTION_ID"}, status = 400)

class CollectionFollowView(View):
    @login_decorator
    def get(self, request, collection_id):
        try:
            if CollectionFollower.objects.filter(Q(user_id = request.user.id) & Q(collection_id = collection_id)).exists():
                CollectionFollower.objects.filter(Q(user_id = request.user.id) & Q(collection_id = collection_id)).delete()
                return HttpResponse(status = 200)
            Collection.objects.get(id = collection_id).collection_follower.add(User.objects.get(id = request.user.id))
            return HttpResponse(status = 200)
        except Collection.DoesNotExist:
            return JsonResponse({"message": "INVALID_COLLECTION_ID"}, status = 400)

