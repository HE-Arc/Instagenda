from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import IgProfile

@receiver(post_save, sender=User)
def create_ig_profile(sender, instance, created, **kwargs):
    if created:
        IgProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_ig_profile(sender, instance, **kwargs):
    instance.profile.save()
