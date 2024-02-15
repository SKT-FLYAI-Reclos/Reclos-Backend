from django.shortcuts import render
from django.core.files import File

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Board
from user.models import User
from .serializers import BoardSerializer

class BoardView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, id=None):
        if id is None:
            boards = Board.objects.all()
            serializer = BoardSerializer(boards, many=True)
            return Response(serializer.data)
        else:
            try:
                board = Board.objects.get(id=id)
            except Board.DoesNotExist:
                return Response({"message": "no board"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = BoardSerializer(board)
            return Response(serializer.data)

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        try:
            board = Board.objects.get(id=id, author=request.user)
        except Board.DoesNotExist:
            return Response({"message": "no board"}, status=status.HTTP_404_NOT_FOUND)
        
        board.delete()
        return Response({"message": "deleted"}, status=status.HTTP_204_NO_CONTENT)



class DummyBoardView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        titles = ["title1", "title2", "title3"]
        contents = ["content1", "content2", "content3"]
        authors = [1, 2, 3]  # Assuming these user IDs exist in your user model
        image_paths = ["./src/ex1.jpg", "./src/ex2.jpg", "./src/ex3.jpg"]  # Adjust paths as necessary
        
        for i in range(3):
            # Open the image file in binary mode
            with open(image_paths[i], 'rb') as img_file:
                board = Board(
                    title=titles[i],
                    content=contents[i],
                    author=User.objects.get(id=authors[i])
                )
                board.image.save(f"ex{i}.jpg", File(img_file), save=False)
                board.save()
        
        return Response({"message": "Dummy boards created successfully"})