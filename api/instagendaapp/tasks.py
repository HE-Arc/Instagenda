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

        # Vérifier si le post n'a pas été supprimé ou s'il est déjà publié
        # if post.date_publication > now():
        #     return {"error": f"Tentative de publication avant l'heure prévue {post.date_publication} - {now()}"}

        # Récupérer l'access token de l'utilisateur (supposons qu'on l'ait stocké dans un autre modèle)
        ig_profile = post.group_owner.owner.profile  # Supposons qu'on ait une relation avec le profil Instagram
        access_token = ig_profile.instagram_access_token

        if not access_token:
            return {"error": "Aucun access_token trouvé pour cet utilisateur"}

        # Étape 1 : Créer un conteneur média
        media_response = requests.post(
            f"{settings.INSTAGRAM_API_URL}/{ig_profile.instagram_user_id}/media",
            data={
                "image_url": post.image_url,  # Récupéré en live depuis la DB
                "caption": post.caption,  # Récupéré en live depuis la DB
                "access_token": access_token
            }
        )
        media_data = media_response.json()

        if "id" not in media_data:
            return {"error": "Erreur lors de la création du conteneur média", "details": media_data}

        container_id = media_data["id"]

        # Étape 2 : Publier le conteneur
        publish_response = requests.post(
            f"{settings.INSTAGRAM_API_URL}/{ig_profile.instagram_user_id}/media_publish",
            data={
                "creation_id": container_id,
                "access_token": access_token
            }
        )

        return publish_response.json()

    except Post.DoesNotExist:
        return {"error": f"Post avec l'ID {post_id} introuvable"}