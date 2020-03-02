import jwt
import json
import requests

from user.models            import User
from card.models            import Style, StyleLike, StyleComment

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

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
                        'description'   : comment.description,
                        'date'          : str(comment.updated_at)[2:11],
                        } for comment in comments.all()]
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
