from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, EmailValidator


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    steps = models.TextField()
    ingredients = models.TextField()

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(validators=[EmailValidator()])
    phone_number = models.CharField(validators=[MinLengthValidator(10)], max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username
