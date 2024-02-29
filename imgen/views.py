import jwt
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.core.files.base import ContentFile

from server import settings
from user.models import User
from .models import ImageRemoveBackground, ImageLadiVton
from .serializers import ImageRemoveBackgroundSerializer, ImageLadiVtonSerializer

import os
import dotenv
import requests

import base64
import io
import uuid

import PIL

dotenv.load_dotenv(override=True)
AI_SERVER_IP = os.getenv('AI_SERVER_IP')

class index(views.APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            print(f'requesting {AI_SERVER_IP}')
            response = requests.get(f'{AI_SERVER_IP}/')
            print(response)
            return Response('AI Server is running', status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response('AI Server is not running', status=status.HTTP_400_BAD_REQUEST)
    

class AIServerInitView(views.APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            response = requests.get(f'{AI_SERVER_IP}/init')
            print('AI Server initialized')
            return Response(response.json(), status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response('AI Server is not initialized', status=status.HTTP_400_BAD_REQUEST)

# id, img
class ImageRemoveBackgroundView(views.APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        serializer = ImageRemoveBackgroundSerializer(ImageRemoveBackground.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        image = request.data.get('image')
        
        if not image:
            return Response({'error': 'Image is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        unique_id = str(uuid.uuid4())
        print(f'unique_id from image remove: {unique_id}')
        
        try:
            response = requests.post(f'{AI_SERVER_IP}/rmbg', files={'image': image}, data={'id': unique_id})
            
            img_data = response.json().get('image')
            if img_data:
                image = PIL.Image.open(io.BytesIO(base64.b64decode(img_data)))
                img_io = io.BytesIO()
                image.save(img_io, format='PNG')
                image_content = ContentFile(img_io.getvalue(), name=f'{unique_id}.png')
                serializer = ImageRemoveBackgroundSerializer(data={'user': request.user.id, 'id': unique_id, 'image': image_content, 'status': 'success'})
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(str(response.json()), status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': 'Image Remove Background failed' + str(e)}, status=status.HTTP_400_BAD_REQUEST)


# uuid[require], category, reference_count
class ImageLadiVtonView(views.APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        serializer = ImageLadiVtonSerializer(ImageLadiVton.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        unique_id = request.data.get('uuid')
        print(f'unique_id from image ladivton: {unique_id}')
        
        if not unique_id:
            return Response({'error': 'uuid is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user.id
        if not user:
            return Response({'error': 'user is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # try:       
        # seg
        clothseg_response = requests.post(f'{AI_SERVER_IP}/clothseg', json={'id': unique_id})
        # print(f'clothseg_response: {clothseg_response.json()}')
        
        #cluster
        category = request.data.get('category')
        print(f'ladivton category: {category}')
        category = 'upper_body' if category == None else category
        if category not in ['upper_body', 'lower_body', 'dresses']:
            return Response({'error': 'category is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
        cluster_response = requests.post(f'{AI_SERVER_IP}/cluster', json={'id': unique_id, 'category' : category})
        # print(f'cluster_response: {cluster_response.json()}')
        
        #LadiVtons
        reference_count = request.data.get('reference_count')
        if not reference_count:
            reference_count = 1
            
        reference_ids = cluster_response.json().get('cluster_id_list')
        
        response = []
        for index in range(reference_count):
            reference_id = reference_ids[index] + "_0"
            ladivton_response = requests.post(f'{AI_SERVER_IP}/ladivton', json={'id': unique_id, 'reference_id': reference_id, 'index':index, 'input_category' : category})
            # print(f'ladivton_response: {ladivton_response.json()}')
            image_data = ladivton_response.json().get('image')
            referene_id = ladivton_response.json().get('reference_id')
            
            """ if not image_data:
                print('No image data')
                return Response('No image data', status=status.HTTP_500_INTERNAL_SERVER_ERROR)"""
            
            image = PIL.Image.open(io.BytesIO(base64.b64decode(image_data)))
            img_io = io.BytesIO()
            image.save(img_io, format='JPEG')
            image_content = ContentFile(img_io.getvalue(), name=f'{unique_id}_{index}.jpg')
            
            serializer_data = {
                'uuid': unique_id, 
                'user': user, 
                'category': category, 
                'image': image_content,
                'reference_id': referene_id,
                'status': 'success'
                }
            
            serializer = ImageLadiVtonSerializer(data=serializer_data)
            
            if serializer.is_valid():
                serializer.save()
                response.append(serializer.data)
                
            """else:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)"""
            
        print(f'response : {response}')
        print(f'I got response!')
        return Response(response, status=status.HTTP_200_OK)
            

        """except Exception as e:
            return Response({'error': 'Image LadiVton failed', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)"""


class ImageLadiVtonByReferenceIdView(views.APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        user = request.user.id
        if not user:
            return Response({'error': 'user is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        image = request.data.get('image')
        if not image:
            return Response({'error': 'image is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        reference_id = request.data.get('reference_id')
        if not reference_id:
            return Response({'error': 'reference_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        print(f'image id : {image}')
        unique_id = image.split("/")[-1].split(".")[0]
        print(f'unique_id from image ladivton by reference_id: {unique_id}')
        print(f'reference id at ladivton by reference_id: {reference_id}')
        
        # try:       
        # seg
        clothseg_response = requests.post(f'{AI_SERVER_IP}/clothseg', json={'id': unique_id})
        # print(f'clothseg_response: {clothseg_response.json()}')
        
        category = request.data.get('category')
        print(f'ladivton by reference_id category: {category}')
        category = 'lower_body' if category == None else category
        if category not in ['upper_body', 'lower_body', 'dresses']:
            return Response({'error': 'category is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
        reference_count = 1
        
        response = []
        for index in range(reference_count):
            ladivton_response = requests.post(f'{AI_SERVER_IP}/ladivton', json={'id': unique_id, 'reference_id': reference_id, 'index':index, 
                                                                                'category': category})
            # print(f'ladivton_response: {ladivton_response.json()}')
            image_data = ladivton_response.json().get('image')
            referene_id = ladivton_response.json().get('reference_id')
            
            """ if not image_data:
                print('No image data')
                return Response('No image data', status=status.HTTP_500_INTERNAL_SERVER_ERROR)"""
            
            image = PIL.Image.open(io.BytesIO(base64.b64decode(image_data)))
            img_io = io.BytesIO()
            image.save(img_io, format='JPEG')
            image_content = ContentFile(img_io.getvalue(), name=f'{unique_id}_{index}.jpg')
            
            serializer_data = {
                'uuid': unique_id, 
                'user': user, 
                'category': category, 
                'image': image_content,
                'reference_id': referene_id,
                'status': 'success'
                }
            
            serializer = ImageLadiVtonSerializer(data=serializer_data)
            
            if serializer.is_valid():
                serializer.save()
                response.append(serializer.data)
                
            """else:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)"""
            
        print(f'response : {response}')
        return Response(response, status=status.HTTP_200_OK)