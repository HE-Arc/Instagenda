from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

# Create your views here.
def backend_status(request):
    return JsonResponse({"status": 'Working!'})

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({"message": "User logged in"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({"error": "Please provide both username and password"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)

    login(request, user)

    return Response({"message": "User registered"}, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
def profile_view(request):
    if request.user.is_authenticated:
        return Response({"username": request.user.username}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({"message": "User logged out"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)