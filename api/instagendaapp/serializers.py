from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Group, Post, IgProfile, PostImage
from django.contrib.auth.hashers import check_password

class IgProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = IgProfile
        fields = ['instagram_access_token', 'instagram_user_id']
        extra_kwargs = {'instagram_access_token': {'write_only': True}, 'instagram_user_id': {'write_only': True}}

class UserSerializer(serializers.ModelSerializer):
    profile = IgProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        # Vérifier si un password est fourni
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)  # Met à jour le mot de passe en le hachant

        # Mise à jour des autres champs
        return super().update(instance, validated_data)

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image', 'order', 'image_url']
        read_only_fields = ['image_url']
    
class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Post
        fields = [
            'id', 'name', 'group_owner', 'caption', 'date_publication', 'status',
            'celery_task_id', 'images', 'uploaded_images'
        ]
        read_only_fields = ['id', 'status', 'group_owner']
        extra_kwargs = {'celery_task_id': {'write_only': True}}

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', None)
        post = Post.objects.create(**validated_data)
        
        if uploaded_images:
            for order, image in enumerate(uploaded_images):
                PostImage.objects.create(post=post, image=image, order=order)
                
        return post
    
class GroupSerializer(serializers.ModelSerializer):
    workers = UserSerializer(many=True, required=False)
    owner = UserSerializer(read_only=True)
    posts = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'owner', 'workers', 'posts']

    def get_posts(self, obj):
        posts = Post.objects.filter(group_owner=obj)
        return PostSerializer(posts, many=True).data

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = self.context['request'].user  # Récupère l'utilisateur connecté

        # Vérifie si l'ancien mot de passe est correct
        if not check_password(data['current_password'], user.password):
            raise serializers.ValidationError({"current_password": "Mot de passe actuel incorrect."})

        # Vérifie si les nouveaux mots de passe correspondent
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"confirm_new_password": "Les mots de passe ne correspondent pas."})

        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])  # Hash et met à jour le mot de passe
        user.save()
        return user
