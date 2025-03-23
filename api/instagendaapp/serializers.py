from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Group, Post, IgProfile

class IgProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = IgProfile
        fields = ['instagram_access_token', 'instagram_user_id']

class UserSerializer(serializers.ModelSerializer):
    profile = IgProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class GroupSerializer(serializers.ModelSerializer):
    workers = UserSerializer(many=True, required=False)
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'owner', 'workers']

class PostSerializer(serializers.ModelSerializer):
    group_owner = GroupSerializer(read_only=True)
    class Meta:
        model = Post
        fields = [
            'id', 'name', 'group_owner', 'caption', 
            'image_url', 'date_publication', 'validated', 'status',
            'celery_task_id'
        ]
        read_only_fields = ['id', 'status', 'group_owner']
        extra_kwargs = {'celery_task_id': {'write_only': True}}