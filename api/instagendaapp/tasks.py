import requests
from celery import shared_task
from django.utils.timezone import now
from django.conf import settings
from .models import Post

@shared_task
def publish_post(post_id):
    try:
        print("task executing...")
        post = Post.objects.get(id=post_id)

        # Récupérer l'access token de l'utilisateur
        instagram_user_id = post.group_owner.owner.profile.instagram_user_id
        access_token = post.group_owner.owner.profile.instagram_access_token

        if not access_token or not instagram_user_id:
            return {"error": "Aucun access_token trouvé pour cet utilisateur"}

        # Étape 1 : Créer un conteneur média
        media_response = requests.post(
            f"{settings.INSTAGRAM_API_URL}/{instagram_user_id}/media",
            data={
                "image_url": post.image_url,
                "caption": post.caption,
                "access_token": access_token
            }
        )
        media_data = media_response.json()

        if "id" not in media_data:
            return {"error": "Erreur lors de la création du conteneur média", "details": media_data}

        container_id = media_data["id"]

        # Étape 2 : Publier le conteneur
        publish_response = requests.post(
            f"{settings.INSTAGRAM_API_URL}/{instagram_user_id}/media_publish",
            data={
                "creation_id": container_id,
                "access_token": access_token
            }
        )

        post.status = "published"
        post.save()

        return publish_response.json()

    except Post.DoesNotExist:
        return {"error": f"Post avec l'ID {post_id} introuvable"}