import json
import requests
import bcrypt
import jwt


from my_settings import SECRET_KEY, KAKAO_KEY
from .models     import User, Follower
from .utils      import login_decorator

from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models       import Q

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(login_id = data['login_id']).exists():
                return JsonResponse({"message":"existing login_id"}, status = 400)

            if len(data['password']) < 7:
                return JsonResponse({"message":"too short password"}, status = 400)

            password_crypt = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            validate_email(data['email'])

            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({"message":"existing email"}, status = 400)

            User(
                login_id  = data['login_id'],
                password  = password_crypt.decode('utf-8'),
                nickname  = data['nickname'],
                email     = data['email'],
                birthday  = data.get('birthday', None),
                gender    = data['gender'],
                image_url = data.get('image_url',None),
            ).save()

            token = jwt.encode({'login_id':data['login_id']}, SECRET_KEY, algorithm = 'HS256')
            return JsonResponse({"token":token.decode('utf-8')}, status = 200)
        except ValidationError:
            return JsonResponse({"message":"INVALID_EMAIL"}, status = 400)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)

class CheckIdView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            login_id = data.get('login_id', None)
            if User.objects.filter(login_id = login_id).exists():
                return JsonResponse({"message": "existing login_id"}, status = 400)
                        
            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

class CheckEmailView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:            
            email = data.get('email', None)
            if User.objects.filter(email = email).exists():
                return JsonResponse({"message": "existing email"}, status = 400)
            
            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

class SignInView(View):
    def post(self, request):
        data     = json.loads(request.body)
        login_id = data.get('login_id', None)
        email    = data.get('email', None)
        try:
            if User.objects.filter(Q(login_id = login_id)|Q(email=email)).exists():
                user = User.objects.filter(Q(login_id = login_id)|Q(email = email))[0]

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'login_id':user.login_id}, SECRET_KEY, algorithm = 'HS256')
                    return JsonResponse({"token":token.decode('utf-8')}, status = 200)
                return HttpResponse(status = 401)
            return HttpResponse(status = 400)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)

class UserFollowView(View):
    @login_decorator
    def get(self, request, followee_id):
        try:
            if Follower.objects.filter(Q(follower_id = request.user.id) & Q(followee_id = followee_id)).exists():
                Follower.objects.filter(Q(follower_id = request.user.id) & Q(followee_id = followee_id)).delete()
                return HttpResponse(status = 200)
            User.objects.get(id = request.user.id).follow_relation.add(User.objects.get(id = followee_id))
            return HttpResponse(status = 200)
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER_ID"}, status = 400)

class CheckSignInIdView(View): 
    def post(self, request):
        try:
            data     = json.loads(request.body)
            login_id = data.get('login_id', None)
            email    = data.get('email', None)

            if User.objects.filter(Q(login_id = login_id)|Q(email=email)).exists():
                return HttpResponse(status = 200)

            return JsonResponse({"message": "not existing account"}, status = 200)
            
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

class KakaoSignInView(View):
    def get(self, request):
        try:
            access_token    = request.headers.get('Authorization', None)
            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"}
            )
            profile_json    = profile_request.json()
            kakao_account   = profile_json.get("kakao_account")
            email           = kakao_account.get("email", None)
            kakao_id        = profile_json.get("id")

            if User.objects.filter(kakao_id = kakao_id).exists():
                user            = User.objects.get(kakao_id = kakao_id)
                token           = jwt.encode({"login_id": user.login_id}, SECRET_KEY, algorithm = "HS256")
                return JsonResponse({"token": token.decode("utf-8")}, status=200)
            user_info           = {"kakao_id" : kakao_id, "email" : email}
            return JsonResponse({"user_info" : user_info}, status = 200)
        except KeyError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status = 400)
        except access_token.DoesNotExist:
            return JsonResponse({"message": "INVALID_TOKEN"}, status = 400)

