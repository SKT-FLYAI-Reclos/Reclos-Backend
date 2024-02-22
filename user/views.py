from dj_rest_auth.registration.views import SocialLoginView

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser

from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from .models import User, Level, Closet
from .serializers import UserSerializer, LevelSerializer, ClosetSerializer

import requests
import jwt
from django.conf import settings

import os
import dotenv
dotenv.load_dotenv()

BASE_URL = os.getenv("BASE_URL")


class UserView(APIView):
    permission_classes = [AllowAny]
    
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
        redirect_uris = [uri.strip() for uri in os.getenv("KAKAO_REDIRECT_URI").split(",")]
        for redirect_uri in redirect_uris:
            token_request = requests.post(
                "https://kauth.kakao.com/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "client_id": os.getenv("KAKAO_REST_API_KEY"),
                    "redirect_uri": redirect_uri,
                    "code": code,
                },
            )
            print(token_request.request.body)
            token_response_json = token_request.json()
            if 'error' in token_response_json:
                continue
            else:
                break
        
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

        response = access_token_return(refresh.access_token, user)
        return response

class UserMyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        access_token = request.headers.get("Authorization")
        if access_token.startswith("Bearer "):
            access_token = access_token.split("Bearer ")[1]

        if not access_token:
            return Response({"error": "No access token provided"}, status=status.HTTP_400_BAD_REQUEST)

        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
        user = User.objects.get(pk=user_id)
        
        return access_token_return(access_token, user)


def refresh_token_return(refresh, user):
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
    
def access_token_return(access_token, user):
    return Response(
        {
            "access": str(access_token),
            "user": {
                "pk": user.pk,
                "username": user.username,
            }
        }
    )

class ClosetView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            closets = Closet.objects.filter(user=user)  # Get all closets for the user
            serializer = ClosetSerializer(closets, many=True)  # Serialize them
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Closet.DoesNotExist:  # This except block is now redundant since filter won't raise DoesNotExist
            return Response({"message": "Closet not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.data)
    
    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
            
            access_token = request.headers.get("Authorization", "").split("Bearer ")[-1]
            if not access_token:
                return Response({"error": "No access token provided"}, status=status.HTTP_400_BAD_REQUEST)
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
            if user.id != payload["user_id"]:
                return Response({"error": "Invalid access token"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClosetSerializer(data=request.data)
        if serializer.is_valid():
            # Assuming your serializer handles the image file correctly
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, id):
        try:
            closet = Closet.objects.get(id=id)
        except Closet.DoesNotExist:
            return Response({"message": "Closet not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClosetSerializer(closet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            closet = Closet.objects.get(id=id)
        except Closet.DoesNotExist:
            return Response({"message": "Closet not found"}, status=status.HTTP_404_NOT_FOUND)
        
        closet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class LevelView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, id=None):
        try:
            user = User.objects.get(id=id)
            level = Level.objects.get(user=user)
            serializer = LevelSerializer(level)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Level.DoesNotExist:
            return Response({"message": "Level not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.data)
    
    def update(self, request, id):
        try:
            user = User.objects.get(id=id)
            level = Level.objects.get(user=user)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Level.DoesNotExist:
            return Response({"message": "Level not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LevelSerializer(level, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DummyDataView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        usernames = ["DummyUser1", "DummyUser2", "DummyUser3", "DummyUser4", "DummyUser5"]
        passwords = ["password1", "password2", "password3", "password4", "password5"]
        closet_categories = ["upper", "bottom", "dress"]
        
        for i in range(5):
            user, created = User.objects.get_or_create(username=usernames[i])
            if created:
                user.set_password(passwords[i])
                user.save()
                
                Level.objects.create(user=user, manner_level=0, water_level=0, tree_level=0)
                
        
        return Response({"message": "User Dummy data created"}, status=status.HTTP_200_OK)
        
class DeleteAllDataView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        User.objects.all().delete()
        Closet.objects.all().delete()
        Level.objects.all().delete()
        
        return Response({"message": "All data deleted"}, status=status.HTTP_200_OK)