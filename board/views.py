from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Board
from .serializers import BoardSerializer

class BoardView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        else:
            return [IsAuthenticated()]
    
    def get(self, request):
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        return Response({"boards": serializer.data})

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