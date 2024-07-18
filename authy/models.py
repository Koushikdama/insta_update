from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from Post.models import Post
from PIL import Image
from django.conf import settings
import os
#dd this import for setting the default value of 'created'

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    profile_pic_name = 'user_{0}/profile.jpg'.format(instance.user.id)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_pic_name

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=80, null=True, blank=True)
    profile_info = models.TextField(max_length=150, null=True, blank=True)
    
    favorites = models.ManyToManyField(Post,null=True,blank=True)
    picture = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='Picture')
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_private=models.CharField(max_length=7,default='public')
    is_send_notifications=models.CharField(max_length=3,default='no')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SIZE = 250, 250

        if self.picture:
            pic = Image.open(self.picture.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.picture.path)

    def __str__(self):
        return self.user.username