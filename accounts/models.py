
from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.utils import upload_to


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to=upload_to, default='avatars/user.png')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

