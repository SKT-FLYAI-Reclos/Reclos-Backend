from django.shortcuts import render
from django.core.files import File

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Board, Images, Likes
from user.models import User
from .serializers import BoardSerializer

class BoardView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, id=None):
        if id is None:
            boards = Board.objects.all().prefetch_related("images", "likes")
            serializer = BoardSerializer(boards, many=True)
            return Response(serializer.data)
        else:
            try:
                board = Board.objects.prefetch_related("images", "likes").get(id=id)
            except Board.DoesNotExist:
                return Response({"message": "no board"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = BoardSerializer(board)
            return Response(serializer.data)

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            board = serializer.save(author=request.user)
            
            images = request.FILES.getlist("images")
            for img in images:
                Images.objects.create(board=board, image=img)
                
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
    
    def post(self, request, id):
        try:
            board = Board.objects.get(id=id)
        except Board.DoesNotExist:
            return Response({"message": "no board"}, status=status.HTTP_404_NOT_FOUND)
        
        like, created = Likes.objects.get_or_create(user=request.user, board=board)
        if not created:
            like.delete()
            return Response({"message": "unliked"})
        return Response({"message": "liked"})


class DummyBoardView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        titles = ["title1", "title2", "title3"]
        contents = ["content1", "content2", "content3"]
        authors = [1, 2, 3]  # Assuming these user IDs exist in your user model
        image_paths = ["./src/ex1.jpg", "./src/ex2.jpg", "./src/ex3.jpg"]  # Adjust paths as necessary
        categories = ["category1", "category2", "category3"]
        
        for i in range(3):
            # Open the image file in binary mode
            with open(image_paths[i], 'rb') as img_file:
                board = Board(
                    title=titles[i],
                    content=contents[i],
                    author=User.objects.get(id=authors[i]),
                    category=categories[i]
                )
                board.save()
                
                if i == 2:
                    img = Images(board=board, image=File(img_file))
                    more_img = Images(board=board, image=File(img_file))
                    img.save()
                    more_img.save()
                
                else:
                    img = Images(board=board, image=File(img_file))
                    img.save()
            
        return Response({"message": "Dummy boards created successfully"})