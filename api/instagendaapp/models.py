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

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    group_owner = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="owned_posts")
    caption = models.TextField()
    image_url = models.URLField()
    date_publication = models.DateTimeField()
    validated = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default="planified")
    celery_task_id = models.IntegerField()

    def __str__(self):
        return f"Post {self.name} planifié à {self.date_publication}"