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
            style_comment = StyleComment.objects.select_related('style', 'user').filter(style_id = style_id)
            comments      = style_comment.filter(style_id = style_id).all() 
            style_user    = style_comment.all()[0].user
            style         = style_comment.all()[0].style
            style = {
                'style_image_url'     : list(style.styleimage_set.values()),
                'related_item'        : list(style.style_related_items.values()),
                'description'         : style.description,
                'profile_image_url'   : style_user.image_url,
                'nickname'            : style_user.nickname,
                'profile_description' : style_user.description,
                'like_count'          : StyleLike.objects.filter(style_id = style_id).count(),
                'comment_count'       : style_comment.count(),
                'comment'             : [
                    {
                        'profile_image' : comment.user.image_url,
                        'nickname'      : comment.user.nickname,
                        'description'   : comment.description,
                        'date'          : str(comment.updated_at)[2:11],
                        } for comment in comments]
                }
            return JsonResponse({"result": style}, status = 200)
        except Style.DoesNotExist:
            return JsonResponse({"message": "INVALID_STYLE_ID"}, status = 400)
