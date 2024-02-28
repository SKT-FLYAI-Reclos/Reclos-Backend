import random
from django.shortcuts import render
from django.core.files import File
from django.core.files.base import ContentFile
import requests

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Board, Image, Like
from user.models import User
from .serializers import BoardSerializer

class BoardView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, id=None):
        if id:
            return self.get_single_board(id)
        else:
            return self.get_boards_by_category(request)
    
    def get_single_board(self, id):
        try:
            board = Board.objects.prefetch_related("images", "likes").get(id=id)
            serializer = BoardSerializer(board)
            return Response(serializer.data)
        except Board.DoesNotExist:
            return Response({"message": "no board"}, status=status.HTTP_404_NOT_FOUND)

    def get_boards_by_category(self, request):
        category = request.query_params.get("category")
        boards = Board.objects.all().prefetch_related("images", "likes")
        if category:
            boards = boards.filter(category=category)
        
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        
        if serializer.is_valid():
            board = serializer.save(author=request.user)
            image_files = request.FILES.getlist("image")
            all_images = request.data.getlist("image")  # This will include both URLs and files
            kinds = request.data.getlist("kind")
            reference_ids = request.data.getlist("reference_id")
            
            print(image_files, all_images, kinds)
            
            # Separate URLs from file names in the all_images list
            image_urls = [img for img in all_images if isinstance(img, str) and img.startswith('http')]

            # Handle the uploaded image files
            for img in image_files:
                reference_id = reference_ids.pop(0)
                print(f'reference_id: {reference_id}')
                Image.objects.create(board=board, image=img, kind=kinds.pop(0), reference_id=reference_id)

            # Now, handle the image URLs
            for img_url in image_urls:
                response = requests.get(img_url)  # Get the image from the URL
                if response.status_code == 200:
                    img_name = img_url.split('/')[-1]  # Extract a simple name from the URL
                    img_temp = ContentFile(response.content, name=img_name)
                    Image.objects.create(board=board, image=img_temp, kind=kinds.pop(0))
            
            esg_water = random.randint(100, 500)
            esg_co2 = random.choice([1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2])
            board.esg_water = esg_water
            board.esg_co2 = esg_co2
            board.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        try:
            board = Board.objects.get(id=id, author=request.user)
        except Board.DoesNotExist:
            return Response({"message": "no board"}, status=status.HTTP_404_NOT_FOUND)
        
        board.delete()
        return Response({"message": "deleted"}, status=status.HTTP_204_NO_CONTENT)


class ToggleLikeView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, id):
        try:
            board = Board.objects.get(id=id)
        except Board.DoesNotExist:
            return Response({"message": "no board"}, status=status.HTTP_404_NOT_FOUND)
        
        likes = board.likes.all()
        return Response({"likes": len(likes)})
    
    def post(self, request, id):
        try:
            board = Board.objects.get(id=id)
        except Board.DoesNotExist:
            return Response({"message": "no board"}, status=status.HTTP_404_NOT_FOUND)
        
        like, created = Like.objects.get_or_create(user=request.user, board=board)
        if not created:
            like.delete()
            return Response({"message": "unliked"})
        return Response({"message": "liked"})


class MyLikeView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        likes = Like.objects.filter(user=request.user)
        boards = [like.board for like in likes]
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
    
class MyLikeByIdView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, id):
        likes = Like.objects.filter(user=request.user, board__id=id)
        if likes:
            return Response({"liked": True})
        return Response({"liked": False})


class DummyBoardView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        titles = ["title1", "title2", "title3"]
        contents = ["content1", "content2", "content3"]
        authors = [1, 2, 3]  # Assuming these user IDs exist in your user model
        image_paths = ["./images/ex1.jpg", "./images/ex2.jpg", "./images/ex3.jpg"]  # Adjust paths as necessary
        categories = ["category1", "category2", "category3"]
        prices = [1000, 2000, 3000]
        
        for i in range(3):
            # Open the image file in binary mode
            with open(image_paths[i], 'rb') as img_file:
                board = Board(
                    title=titles[i],
                    content=contents[i],
                    author=User.objects.get(id=authors[i]),
                    category=categories[i],
                    price=prices[i]
                )
                board.save()
                
                if i == 2:
                    img = Image(board=board, image=File(img_file))
                    more_img = Image(board=board, image=File(img_file))
                    img.save()
                    more_img.save()
                
                else:
                    img = Image(board=board, image=File(img_file))
                    img.save()
            
        return Response({"message": "Dummy boards created successfully"})
