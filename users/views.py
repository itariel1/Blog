from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserRegistrSerializer, UserListSerializer

class UserListAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def user_item_view(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(data={'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    data = UserListSerializer(user).data
    return Response(data=data)

class RegistrUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)