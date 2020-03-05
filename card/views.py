import jwt
import json
import requests
import boto3
import uuid

from user.models              import User, Follower
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
from my_settings              import aws_access_key_id, aws_secret_access_key, aws_s3_address

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
            collection_style_list = CollectionStyle.objects.filter(style_id = style_id).all()
            style = {
                'style_image_url'     : [style.image_url for style in styles],
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
                        'description'   : comment.description,
                        'date'          : str(comment.user.updated_at)[2:11],
                    } for comment in style_comments],
                'collection'          : [
                    {
                        'id'            : collection_style.collection.id,
                        'name'          : collection_style.collection.name,
                        'image_url'     : collection_style.collection.image_url
                    } for collection_style in collection_style_list]
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
                'style_image_url'    : list(style.styleimage_set.values('image_url')),
                'style_description'  : style.description,
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

class DailyLookCollectionView(View):
    def get(self, request):
        ordered_collection_list = Collection.objects.prefetch_related('collection_follower', 'collection_style')\
                                  .annotate(follower_count = Count('collection_follower')).order_by('-follower_count')
        collection_list = [
            {
                'collection_id'        : collection.id,
                'collection_name'      : collection.name,
                'collection_image_url' : collection.image_url,
                'description'          : collection.description,
                'profile_image_url'    : collection.user.image_url,
                'nickname'             : collection.user.nickname,
                'style_count'          : collection.collection_style.count() ,
                'follower_count'       : collection.collection_follower.count()
            }
            for collection in ordered_collection_list[:10]]
        return JsonResponse({"collection_list": collection_list}, status = 200)

class NewCardView(View):
    def get(self, request):
        style_list = Style.objects.all().prefetch_related('style_related_items', 'comments').order_by('-created_at')
        card_list = [
            {
                'style_id'           : style.id,
                'style_image_url'    : list(style.styleimage_set.values('image_url')),
                'style_description'  : style.description,
                'related_item'       : list(style.style_related_items.values()),
                'profile_image_url'  : style.user.image_url,
                'nickname'           : style.user.nickname,
                'profile_description': style.user.description,
                'date'               : str(style.created_at)[2:11],
                'like_count'         : style.style_like.count(),
                'comment_count'      : style.comments.count(),
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

class FollowingCardView(View):
    @login_decorator
    def get(self, request):
        followee_list = Follower.objects.filter(follower_id = request.user.id)
        followee_id_list = [followee.followee.id for followee in followee_list]
        style_list = Style.objects.filter(user_id__in=followee_id_list).prefetch_related('user','comments').order_by('-created_at')
        card_list = [
            {
                'style_id'           : style.id,
                'style_image_url'    : list(style.styleimage_set.values('image_url')),
                'style_description'  : style.description,
                'related_item'       : list(style.style_related_items.values()),
                'profile_image_url'  : style.user.image_url,
                'nickname'           : style.user.nickname,
                'profile_description': style.user.description,
                'date'               : str(style.created_at)[2:11],
                'like_count'         : style.style_like.count(),
                'comment_count'      : style.comments.count(),
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

            for image in data['image_url_list']:
                StyleImage.objects.create(
                    image_url = image,
                    style_id = make.id
            )
            related_items = random_item()
            StyleRelatedItem.objects.create(
                pants        = related_items['pants'],
                skirt        = related_items['skirt'],
                shoes        = related_items['shoes'],
                bag          = related_items['bag'],
                accessory    = related_items['accessory'],
                etc          = related_items['etc'],
                style_id     = make.id
            )
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)
        return HttpResponse(status = 200)

class ImageUploadView(View):
    s3_client = boto3.client(
        's3',
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key,
    )
    @login_decorator
    def post(self, request):
        image_url_list = []
        for file in request.FILES.getlist('filename'):
            url_generator = str(uuid.uuid4())
            self.s3_client.upload_fileobj(
                file,
                "wetyle-share",
                url_generator,
                ExtraArgs={
                    "ContentType": file.content_type
                }
            )
            image_url_list.append(f'{aws_s3_address}{url_generator}')
        return JsonResponse({"image_url_list":image_url_list}, status= 200)

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
                'style_image_url'    : list(style.styleimage_set.values('image_url')),
                'style_description'  : style.description,
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
                    'style_image_url'    : list(style.styleimage_set.values('image_url')),
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

class SearchCollectionView(View):
    def get(self, request):
        query = request.GET.get('query', None)
        searched_list = Collection.objects.filter(Q(name__icontains = query) | Q(description__icontains = query)).all()
        collection_list = [
            {
                'collection_id'        : collection.id,
                'collection_name'      : collection.name,
                'collection_image_url' : collection.image_url,
                'description'          : collection.description,
                'profile_image_url'    : collection.user.image_url,
                'nickname'             : collection.user.nickname,
                'style_count'          : collection.collection_style.count() ,
                'follower_count'       : collection.collection_follower.count()
            } for collection in searched_list]
        return JsonResponse({"result" : collection_list}, status = 200)

class CollectionUploadView(View):
    @login_decorator
    def post(self,request):
        data = json.loads(request.body)
        try:
            Collection.objects.create(
                name         = data['name'],
                image_url    = data['image_url'],
                description  = data['description'],
                user_id      = request.user.id
            )
            return HttpResponse(status = 200)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)
