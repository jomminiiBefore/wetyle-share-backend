import json
import requests
import bcrypt
import jwt

from my_settings import SECRET_KEY
from .models import User

from django.views import View
from django.http import JsonResponse, HttpResponse

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try :
            if User.objects.filter(login_id = data['login_id']).exists():
                return HttpResponse(status = 400)

            password_crypt = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

            if User.objects.filter(email = data['email']).exists():
                return HttpResponse(status = 400)

            User(
                login_id = data['login_id'],
                password = password_crypt.decode('utf-8'),
                nickname = data['nickname'],
                email    = data['email'],
                birthday = data.get('birthday', None),
                gender   = data['gender'],
                image    = data['image'],
            ).save()

            token = jwt.encode({'login_id' : user.login_id}, SECRET_KEY, algorithm = 'HS256')

            return JsonResponse({"token" : token.decode('utf-8')}, status = 200)

        except KeyError :
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

