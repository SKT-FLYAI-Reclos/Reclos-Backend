from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import ImageRemoveBackground, ImageLadiVton
from .serializers import ImageRemoveBackgroundSerializer, ImageLadiVtonSerializer

import os
import dotenv
import requests

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
    
    def post(self, request):
        image = request.data.get('image')
        id = request.data.get('id')
        
        if not image:
            return Response({'error': 'Image is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not id:
            return Response({'error': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            response = requests.post(f'{AI_SERVER_IP}/rmbg', files={'image': image}, data={'id': id})
            print(response.json())
            return Response(response.json(), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Image Remove Background failed'}, status=status.HTTP_400_BAD_REQUEST)

class ImageLadiVtonView(views.APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        id = request.data.get('id')
        
        if not id:
            return Response({'error': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # seg
            clothseg_response = requests.post(f'{AI_SERVER_IP}/clothseg', json={'id': id})
            print(f'clothseg_response: {clothseg_response.json()}')
            
            #cluster
            category = request.data.get('category')
            category = 'upper_body' if category == None else category
            if category not in ['upper_body', 'lower_body', 'dresses']:
                return Response({'error': 'category is invalid'}, status=status.HTTP_400_BAD_REQUEST)
            
            cluster_response = requests.post(f'{AI_SERVER_IP}/cluster', json={'id': id, 'category' : category})
            print(f'cluster_response: {cluster_response.json()}')
            
            #LadiVton
            reference_id = request.data.get('reference_id')
            reference_id = '000000_0' if reference_id == None else reference_id
            ladivton_response = requests.post(f'{AI_SERVER_IP}/ladivton', json={'id': id, 'reference_id': reference_id})
            print(f'ladivton_response: {ladivton_response.json()}')
            
            return Response(ladivton_response.json(), status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': 'Image LadiVton failed'}, status=status.HTTP_400_BAD_REQUEST)