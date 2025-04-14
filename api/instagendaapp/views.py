from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import UserSerializer, GroupSerializer, PostSerializer, ChangePasswordSerializer, PostImageSerializer
from .models import IgProfile, Group, Post, PostImage
import requests
from django.conf import settings
from django.utils.timezone import make_aware
from datetime import datetime
from django.utils.timezone import now
from celery import current_app
from .tasks import publish_post
import pytz
import os

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
            return Response({"message": "Utilisateur connecté"}, status=status.HTTP_200_OK)
        return Response({"error": "Champs invalides"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({"message": "Utilisateur enregistré"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({"message": "Utilisateur déconnecté"}, status=status.HTTP_200_OK)
        return Response({"error": "Utilisateur non déconnecté"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        if not request.user or request.user.is_anonymous:
            return Response({"error": "Utilisateur non authentifié"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class IgViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def connection(self, request):
        if not request.user or request.user.is_anonymous:
            return Response({"error": "Utilisateur non authentifié"}, status=status.HTTP_401_UNAUTHORIZED)
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
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def status(self, request):
        try:
            ig_profile = request.user.profile

            if ig_profile.instagram_access_token and ig_profile.instagram_user_id:
                # Si le username est vide, on le récupère depuis l'API Meta
                if not ig_profile.instagram_username:
                    url = f"{settings.INSTAGRAM_API_URL}/{ig_profile.instagram_user_id}"
                    params = {
                        "fields": "username",
                        "access_token": ig_profile.instagram_access_token
                    }

                    response = requests.get(url, params=params)
                    if response.status_code == 200:
                        data = response.json()
                        username = data.get("username")
                        if username:
                            ig_profile.instagram_username = username
                            ig_profile.save()
                    else:
                        return Response({
                            "connected": False,
                            "error": "Erreur lors de la récupération du nom d'utilisateur depuis Instagram."
                        }, status=response.status_code)
                return Response({
                    "connected": True,
                    "username": ig_profile.instagram_username
                })

        except IgProfile.DoesNotExist:
            pass

        return Response({
            "connected": False,
            "message": "Aucun compte Instagram lié"
        })


    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def disconnect(self, request):
        try:
            ig_profile = request.user.profile
            ig_profile.instagram_access_token = None
            ig_profile.instagram_user_id = None
            ig_profile.instagram_username = None
            ig_profile.save()
            return Response({"message": "Compte Instagram déconnecté avec succès."})
        except IgProfile.DoesNotExist:
            return Response({"error": "Aucun compte à déconnecter."}, status=404)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        user = self.get_object()
        data = UserSerializer(user).data

        if user.id != request.user.id:
            return Response({'error': 'Vous n\'êtes pas autorisé à accéder à cet utilisateur.'}, status=status.HTTP_403_FORBIDDEN)
        
        return Response(data)
    
    def update(self, request, pk=None):
        user = request.user

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Mot de passe mis à jour avec succès."}, status=status.HTTP_200_OK)

class GroupViewSet(viewsets.ModelViewSet):
    
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        group = self.get_object()
        data = GroupSerializer(group).data

        if not hasRights(group, request):
            return Response({'error': 'Vous n\'êtes pas un membre du groupe.'}, status=status.HTTP_403_FORBIDDEN)
        
        return Response(data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return (Group.objects.filter(owner=user) | Group.objects.filter(workers__in=[user])).distinct()
    
    def destroy(self, request, *args, **kwargs):
        group = self.get_object()

        if group.owner.id != request.user.id:
            return Response({'error': 'Vous n\'êtes pas le propriétaire du groupe.'}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(group)
        return Response({'status': 'Group deleted'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['put'])
    def add_user(self, request, pk=None):
        group = self.get_object()
        user_username = request.data.get('username')

        if group.owner.id != request.user.id:
            return Response({'error': 'Vous n\'êtes pas le propriétaire du groupe.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(username=user_username)

            if group.workers.filter(id=user.id).exists():
                return Response({'error': 'L\'utilisateur est déjà dans le groupe'}, status=status.HTTP_400_BAD_REQUEST)
            
            group.workers.add(user)
            return Response({'user': UserSerializer(user).data})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)

    @action(detail=True, methods=['put'])
    def remove_user(self, request, pk=None):
        group = self.get_object()
        user_id = request.data.get('user_id')

        if group.owner.id != request.user.id:
            return Response({'error': 'Vous n\'êtes pas le propriétaire du groupe.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=user_id)
            group.workers.remove(user)
            return Response({'status': 'Utilisateur enlevé'})
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur introuvable'}, status=400)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def perform_create(self, serializer):
        name = self.request.data.get("name")
        caption = self.request.data.get("caption")
        date_str = self.request.data.get("date_publication")
        group_id = self.request.data.get("group_id")
        group_owner = Group.objects.get(id=group_id)

        if not hasRights(group_owner, self.request):
            return Response({'error': 'Vous n\'êtes pas autorisé à créer un post dans ce groupe'}, status=status.HTTP_403_FORBIDDEN)

        date_publication_aw = make_aware(datetime.strptime(date_str, "%Y-%m-%d %H:%M"), timezone=pytz.timezone('UTC'))
        date_publication = date_publication_aw.astimezone(pytz.utc)

        post = serializer.save(name=name, caption=caption, group_owner=group_owner, date_publication=date_publication)

        task = publish_post.apply_async(
            args=[post.id],
            eta=date_publication
        )

        post.celery_task_id = task.id
        post.save()

    def retrieve(self, request, pk=None):
        post = self.get_object()
        group = post.group_owner

        if not hasRights(group, request):
            return Response(
                {'error': 'Vous n\'êtes pas autorisé à accéder à ce post'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(post)
        return Response(serializer.data)
      
    def update(self, request, pk=None):
        post = self.get_object()
        group = post.group_owner

        if not hasRights(group, request):
            return Response({'error': 'Vous n\'êtes pas autorisé à éditer ce post'}, status=status.HTTP_403_FORBIDDEN)
        
        old_date = post.date_publication

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            updated_post = serializer.save()

            date_str = request.data.get("date_publication")
            new_date_aw = make_aware(datetime.strptime(date_str, "%Y-%m-%d %H:%M"), timezone=pytz.timezone('UTC'))
            new_date = new_date_aw.astimezone(pytz.utc)

            if old_date != new_date and new_date > now():
                if post.celery_task_id:
                    try:
                        current_app.control.revoke(post.celery_task_id, terminate=True)
                    except Exception as e:
                        pass

                task = publish_post.apply_async(args=[post.id], eta=new_date)
                updated_post.celery_task_id = task.id
                updated_post.date_publication = new_date

            uploaded_images = request.FILES.getlist("uploaded_images")
            if uploaded_images:
                old_images = list(PostImage.objects.filter(post=post).order_by('order'))

                is_different = (
                    len(uploaded_images) != len(old_images) or
                    any(
                        uploaded_images[i].name != old_images[i].image.name.split('/')[-1] or
                        uploaded_images[i].size != old_images[i].image.size
                        for i in range(min(len(uploaded_images), len(old_images)))
                    )
                )

                if is_different:
                    for image in old_images:
                        try:
                            image.image.delete(save=False)
                        except Exception as e:
                            print(f"Erreur lors de la suppression d'une image : {e}")
                    PostImage.objects.filter(post=post).delete()

                    for order, image in enumerate(uploaded_images):
                        PostImage.objects.create(post=post, image=image, order=order)

            updated_post.status = "unvalidated"
            updated_post.save()
            return Response(PostSerializer(updated_post).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        group = post.group_owner

        if not hasRights(group, request):
            return Response({'error': 'Vous n\'êtes pas autorisé à supprimer ce post'}, status=status.HTTP_403_FORBIDDEN)
        
        # Delete Celery task if it exists
        if post.celery_task_id:
            try:
                current_app.control.revoke(post.celery_task_id, terminate=True)
            except Exception as e:
                pass
        
        images = PostImage.objects.filter(post=post)

        for image in images:
            try:
                image.image.delete(save=False)
            except Exception as e:
                print(f"Error deleting image: {e}")
        
        post_folder = os.path.join(settings.MEDIA_ROOT, 'post_images', str(post.id))
        if os.path.exists(post_folder):
            os.rmdir(post_folder)
        
        # Delete the post (this will also delete the PostImage relations in cascade)
        self.perform_destroy(post)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def list(self, request, *args, **kwargs):
        return Response({'detail': 'Accès à cet endpoint non autorisé.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        post = self.get_object()
        images = PostImage.objects.filter(post=post)
        serializer = PostImageSerializer(images, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put'])
    def validate(self, request, pk=None):
        post = self.get_object()
        group = post.group_owner

        # Vérifie que l'utilisateur est bien le propriétaire du groupe
        if group.owner.id != request.user.id:
            return Response({'error': 'Vous n\'êtes pas autorisé à valider ce post.'}, status=status.HTTP_403_FORBIDDEN)

        # Vérifie que l'utilisateur a un profil Instagram lié
        try:
            ig_profile = request.user.profile
            if not ig_profile.instagram_access_token or not ig_profile.instagram_user_id:
                raise AttributeError()
        except (IgProfile.DoesNotExist, AttributeError):
            return Response(
                {'error': 'Vous devez lier un compte Instagram avant de valider un post. Veuillez vous rendre dans la page de profil.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        post.status = 'validated'
        post.save()

        return Response({'message': 'Post validé avec succès.', 'status': post.status}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def unvalidate(self, request, pk=None):
        post = self.get_object()
        group = post.group_owner

        if group.owner.id != request.user.id:
            return Response({'error': 'Vous n\'êtes pas autorisé à dévalider ce post.'}, status=status.HTTP_403_FORBIDDEN)

        post.status = 'unvalidated'
        post.save()

        return Response({'message': 'Post dévalidé avec succès.', 'status': post.status}, status=status.HTTP_200_OK)

def hasRights(group, request):
    is_owner = group.owner.id == request.user.id
    is_worker = group.workers.filter(id=request.user.id).exists()
    return is_owner or is_worker