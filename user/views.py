import json
import requests
import bcrypt
import jwt

from my_settings import SECRET_KEY
from .models import User
from .utils import login_decorator

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

class KakaoSignInView(View):
    def get(self, request):
        try:
            access_token = request.headers.get('Authorization', None)

            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me", headers = {"Authorization" : f"Bearer {access_token}"},
            )
            profile_json = profile_request.json()

            kakao_account = profile_json.get("kakao_account")
            kakao_id = profile_json.get("id")
            email    = kakao_account.get("email", None)

        except KeyError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status = 400)

        except access_token.DoesNotExist:
            return JsonResponse({"message": "INVALID_TOKEN"}, status = 400)

        if User.objects.filter(kakao_id = kakao_id).exists():
            user = User.objects.get(kakao_id = kakao_id)
            token = jwt.encode({"login_id" : user.login_id}, SECRET_KEY, algorithm = 'HS256')
            token = token.decode('utf-8')

            return JsonResponse({"token" : token}, status = 200)

        else :
            return JsonResponse({"kakao_id": kakao_id, "email" : email}, status = 200)

class KakaoSignInAddView(View):
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
                kakao_id = data['kakao_id'],
            ).save()

            # 가입 완료되면 바로 토큰 발행
            token = jwt.encode({'login_id' : user.login_id}, SECRET_KEY, algorithm = 'HS256')
            token = token.decode('utf-8')

            return JsonResponse({"token" : token}, status = 200)

        except KeyError :
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

