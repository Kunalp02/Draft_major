from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=10, unique=True, null=True, default=None)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=10)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    curr_class = models.CharField(max_length=50, null=True, blank=True)
    board = models.CharField(max_length=50, blank=True)
    skills = models.CharField(max_length=255, blank=True)
    certifications = models.TextField(blank=True)
    hobbies = models.CharField(max_length=255, blank=True)
    school = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.fname} {self.lname}'s Profile"

    def __str__(self):
        return self.user.username
