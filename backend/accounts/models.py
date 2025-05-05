from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import uuid

class Activation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Activation for {self.user.username}"
    



class User(AbstractUser):
    activation_code = models.CharField(max_length=64, blank=True, null=True)

     # Add related_name to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group', related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='custom_user_permissions_set', blank=True)

