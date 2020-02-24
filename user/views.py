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

            # 비밀번호 암호화
            password_crypt = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            password_crypt = password_crypt.decode('utf-8')

            User(
                login_id = data['login_id'],
                password = password_crypt,
                nickname = data['nickname'],
                email = data['email'],
                birthday = data.get('birthday', None),
                sex = data['sex'],
                image = data['image'],
            ).save()

            # 가입 완료되면 바로 토큰 발행
            token = jwt.encode({'login_id' : user.login_id}, SECRET_KEY, algorithm = 'HS256')
            token = token.decode('utf-8')

            return JsonResponse({"token" : token}, status = 200)

        except KeyError :
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
           if User.objects.filter(login_id = data['login_id']).exists():
               user = User.objects.get(login_id = data['login_id'])


               if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                   # 토큰 발행
                   token = jwt.encode({'login_id' : user.login_id}, SECRET_KEY, algorithm = 'HS256')
                   token = token.decode('utf-8')

                   return JsonResponse({"token" : token}, status = 200)

               else :
                   return HttpResponse(status = 401)
        except KeyError :
            return  HttpResponse(status = 400)

