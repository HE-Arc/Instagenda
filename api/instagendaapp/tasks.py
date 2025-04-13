import requests
from celery import shared_task
from django.conf import settings
from .models import Post, PostImage

@shared_task
def publish_post(post_id):
    try:
        print("task executing...")
        post = Post.objects.get(id=post_id)

        if post.status != "validated":
            updateStatus(post, "expired")
            return {"error": "Le post n'a pas été encore validé"}

        # Récupérer l'access token de l'utilisateur
        instagram_user_id = post.group_owner.owner.profile.instagram_user_id
        access_token = post.group_owner.owner.profile.instagram_access_token

        if not access_token or not instagram_user_id:
            updateStatus(post, "expired")
            return {"error": "Aucun access_token trouvé pour cet utilisateur"}
        
        # Récupérer les images du post
        images = PostImage.objects.filter(post=post)

        media_container = []
        for image in images:
            # Créer un conteneur pour chaque image (et si il y a plusieurs images, créer les objets carousel)
            image_data = {
                "image_url": f"{settings.BACKEND_URL}/{image.image_url}",
                "access_token": access_token,
                "is_carousel_item": len(images) > 1
            }
            if len(images) == 1:
                image_data["caption"] = post.caption

            image_response = requests.post(
                f"{settings.INSTAGRAM_API_URL}/{instagram_user_id}/media",
                data=image_data
            )
            image_data = image_response.json()
            if "id" not in image_data:
                updateStatus(post, "expired")
                return {"error": "Erreur lors de la création du conteneur", "details": image_data}
            media_container.append(image_data["id"])

        container_id = None

        # Si le media_container contient plusieurs images, on crée un conteneur carousel
        if len(media_container) != 1:
            # Sinon, on crée un conteneur carousel avec toutes les images
            carousel_container = requests.post(
                f"{settings.INSTAGRAM_API_URL}/{instagram_user_id}/media",
                data={
                    "media_type": "CAROUSEL",
                    "children": ",".join(media_container),
                    "access_token": access_token,
                    "caption": post.caption,
                }
            )
            carousel_data = carousel_container.json()
            if "id" not in carousel_data:
                updateStatus(post, "expired")
                return {"error": "Erreur lors de la création du conteneur carousel", "details": carousel_data}
            container_id = carousel_data["id"]
        else:
            container_id = media_container[0]
        
        if not container_id:
            updateStatus(post, "expired")
            return {"error": "Erreur lors de la création du conteneur"}
        
        # Puis on publie le post
        publish_response = requests.post(
            f"{settings.INSTAGRAM_API_URL}/{instagram_user_id}/media_publish",
            data={
                "creation_id": container_id,
                "access_token": access_token
            }
        )
        if publish_response.status_code != 200:
            updateStatus(post, "expired")
            return {"error": "Erreur lors de la publication du post", "details": publish_response.json()}

        updateStatus(post, "published")

        return publish_response.json()

    except Post.DoesNotExist:
        return {"error": f"Post avec l'ID {post_id} introuvable"}
    
def updateStatus(post, status):
    post.status = status
    post.save()