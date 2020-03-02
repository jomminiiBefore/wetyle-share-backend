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
            
            style_comments = Style.objects.prefetch_related('comments').get(id=style_id).comments.all()
            
            # style_user    = Style.objects.get(id=style_id)
            style_image    = Style.objects.prefetch_related('styleimage_set').get(id=style_id)

            like_count = StyleLike.objects.filter(style_id = style_id).count()

            style = {
                # 'style_image_url'     : list(style.styleimage_set.values()),
                # 'related_item'        : list(style.style_related_items.values()),

                # 'description'         : style.description,
                'profile_image_url'   : style_image.styleimage_set.get().image_url,
                'nickname'            : style_image.user.nickname,
                'profile_description' : style_image.user.description,

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
