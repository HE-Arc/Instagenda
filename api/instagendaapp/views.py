from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializers import UserSerializer, GroupSerializer, PostSerializer
from .models import IgProfile, Group, Post
import requests
from django.conf import settings
from django.utils.timezone import make_aware
from datetime import datetime
from celery import current_app
from .tasks import publish_post
import pytz

# Create your views here.
def backend_status(request):
    return JsonResponse({"status": 'Working!'})

class AuthViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "User logged in"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({"message": "User registered"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({"message": "User logged out"}, status=status.HTTP_200_OK)
        return Response({"error": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        if not request.user or request.user.is_anonymous:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class IgViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def connection(self, request):
        if not request.user or request.user.is_anonymous:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        code = request.data.get('code')

        client_id = settings.INSTAGRAM_CLIENT_ID
        client_secret = settings.INSTAGRAM_CLIENT_SECRET
        redirect_uri = settings.INSTAGRAM_REDIRECT_URI
        grant_type = 'authorization_code'

        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': grant_type,
            'redirect_uri': redirect_uri,
            'code': code
        }

        response = requests.post(settings.INSTAGRAM_SHORT_TOKEN_URL, data=payload)

        if response.status_code == 200:
            # redo the same to get long-lived token
            payload = {
                'client_secret': client_secret,
                'grant_type': "ig_exchange_token",
                'access_token': response.json().get('access_token')
            }
            long_lived_response = requests.get(settings.INSTAGRAM_LONG_TOKEN_URL, params=payload)

            if long_lived_response.status_code == 200:
                data = long_lived_response.json()
                long_lived_token = data.get('access_token')

                payload = {
                    'fields': 'id',
                    'access_token': long_lived_token
                }

                instagram_id_response = requests.get(settings.INSTAGRAM_USER_ID_URL, params=payload)
                if instagram_id_response.status_code == 200:
                    data = instagram_id_response.json()
                    instagram_user_id = data.get('id')
                    ig_profile, created = IgProfile.objects.get_or_create(user=request.user)
                    ig_profile.instagram_access_token = long_lived_token
                    ig_profile.instagram_user_id = instagram_user_id
                    ig_profile.save()

                    return Response(long_lived_response.json(), status=status.HTTP_200_OK)
                return Response(instagram_id_response.json, status=instagram_id_response.status_code)
            return Response(long_lived_response.json(), status=long_lived_response.status_code)
        return Response(response.json(), status=response.status_code)

class GroupViewSet(viewsets.ModelViewSet):
    
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        group = self.get_object()
        data = GroupSerializer(group).data

        is_owner = data["owner"]["id"] == request.user.id
        is_worker = any(worker["id"] == request.user.id for worker in data["workers"])
        if not (is_owner or is_worker):
            return Response({'error': 'You are not the owner of this group'}, status=status.HTTP_403_FORBIDDEN)
        
        return Response(data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return (Group.objects.filter(owner=user) | Group.objects.filter(workers__in=[user])).distinct()
    
    def destroy(self, request, *args, **kwargs):
        group = self.get_object()

        if group.owner.id != request.user.id:
            return Response({'error': 'You are not the owner of this group'}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(group)
        return Response({'status': 'Group deleted'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['put'])
    def add_user(self, request, pk=None):
        group = self.get_object()
        user_username = request.data.get('username')

        if group.owner.id != request.user.id:
            return Response({'error': 'You are not the owner of this group'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(username=user_username)

            if group.workers.filter(id=user.id).exists():
                return Response({'error': 'User is already in the group'}, status=status.HTTP_400_BAD_REQUEST)
            
            group.workers.add(user)
            return Response({'user': UserSerializer(user).data})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)

    @action(detail=True, methods=['put'])
    def remove_user(self, request, pk=None):
        group = self.get_object()
        user_id = request.data.get('user_id')

        if group.owner.id != request.user.id:
            return Response({'error': 'You are not the owner of this group'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=user_id)
            group.workers.remove(user)
            return Response({'status': 'User removed'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)

class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        name = self.request.data.get("name")
        caption = self.request.data.get("caption")
        image_url = self.request.data.get("image_url")
        date_str = self.request.data.get("date_publication")
        group_owner_id = self.request.data.get("group_owner_id")

        date_publication_aw = make_aware(datetime.strptime(date_str, "%Y-%m-%d %H:%M"), timezone=pytz.timezone('UTC'))
        date_publication = date_publication_aw.astimezone(pytz.utc)

        group_owner = Group.objects.get(id=group_owner_id)

        post = serializer.save(name=name, caption=caption, group_owner=group_owner, image_url=image_url, date_publication=date_publication)

        task = publish_post.apply_async(
            args=[post.id],
            eta=date_publication
        )

        post.celery_task_id = task.id
        post.save()