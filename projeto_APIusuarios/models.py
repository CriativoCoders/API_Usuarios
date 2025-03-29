from django.db import models
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    education = models.CharField(max_length=100, blank=True)
    pets_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username