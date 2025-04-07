from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Group
from django.contrib.auth.hashers import check_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
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
    
class GroupSerializer(serializers.ModelSerializer):
    workers = UserSerializer(many=True, required=False)
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'owner', 'workers']

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