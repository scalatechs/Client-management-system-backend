from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from apps.accounts.models import CustomUser
from .serializers import CustomUserSerializer, SignInSerializer

# Create your views here.
class SignUp_In(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        refresh = RefreshToken.for_user(user) 
        return Response(
            {
                "message":"User Created successfull !",
                "user":CustomUserSerializer(user).data,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['POST'], url_path='sign-in')
    def sign_in(self,request):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user= serializer.validated_data['user']
        login(request,user)
        refresh = RefreshToken.for_user(user) 
        return Response(
            {
                "message":"User Logged in successfully !", 
                "user":CustomUserSerializer(user).data,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            },
    
            status=status.HTTP_200_OK
        )


