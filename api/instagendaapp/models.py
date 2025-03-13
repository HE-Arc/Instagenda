from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class IgProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    instagram_access_token = models.CharField(max_length=255, blank=True, null=True)
    instagram_user_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    
class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_groups")
    workers = models.ManyToManyField(User, related_name="work_groups")

    def __str__(self):
        return self.name