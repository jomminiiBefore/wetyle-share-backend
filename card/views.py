import jwt
import json
import requests

from user.models            import User
from card.models            import Style, StyleLike, StyleComment

from django.views           import View
from django.http            import JsonResponse

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
