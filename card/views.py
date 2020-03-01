import jwt
import json
import requests

from user.models            import User
from card.models            import Style, StyleLike

from django.views           import View
from django.http            import JsonResponse

class StyleView(View):
    def get(self, request, style_id):
        try:
            request_style = Style.objects.get(id = style_id)
            style_user    = Style.objects.select_related('user').get(id = style_id).user
            comments      = Style.objects.prefetch_related('comments')\
                            .select_related('user').get(id = style_id).comments
            style = {
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
                }
            return JsonResponse({"result": style}, status = 200)
        except Style.DoesNotExist:
            return JsonResponse({"message": "INVALID_STYLE_ID"}, status = 400)
