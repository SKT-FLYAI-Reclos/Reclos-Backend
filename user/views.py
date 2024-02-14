from dj_rest_auth.registration.views import SocialLoginView

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from .models import User
from .serializers import UserSerializer

import requests
import jwt
from django.conf import settings

import os
import dotenv
dotenv.load_dotenv()

BASE_URL = os.getenv("BASE_URL")

class UserView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        else:
            return [IsAuthenticated()]
    
    def get(self, request, id=None):
        if id:
            try:
                user = User.objects.get(id=id)
                serializer = UserSerializer(user)
            except User.DoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
        
        return Response(serializer.data)

class KakaoLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return Response({"error": "Code not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Exchange the code for a token
        token_request = requests.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": os.getenv("KAKAO_REST_API_KEY"),
                "redirect_uri": "http://localhost:3000/login/kakao-callback",
                "code": code,
            },
        )
        token_response_json = token_request.json()
        if 'error' in token_response_json:
            return Response(token_response_json, status=status.HTTP_400_BAD_REQUEST)

        access_token = token_response_json.get("access_token")

        # Use the access token to get the user's info from Kakao
        user_info_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_info_json = user_info_request.json()
        username = user_info_json.get("properties", {}).get("nickname", "")

        if not username:
            return Response({"error": "Failed to retrieve username from Kakao"}, status=status.HTTP_400_BAD_REQUEST)

        # Create or get the user
        user, created = User.objects.get_or_create(username=username)
        refresh = RefreshToken.for_user(user)

        response = token_return(refresh, user)
        response.set_cookie(
            "refresh_token",
            str(refresh),
            httponly=False,
            secure=False,
            samesite="None",
        )
        
        return response

class UserMyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token_cookie = self.request.COOKIES.get("refresh_token")

        if not token_cookie:
            return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)

        payload = jwt.decode(token_cookie, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
        user = User.objects.get(pk=user_id)
        refresh = RefreshToken.for_user(user)

        return token_return(refresh, user)


def token_return(refresh, user):
    return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "pk": user.pk,
                "username": user.username,
            }
        }
    )