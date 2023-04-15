"""
Module for forms related to the recipes app.

R0903: Too few public methods (0/2) (too-few-public-methods)
These warnings are related to the number of public methods in the form classes.
A public method is a method that can be accessed outside of the class.
The linter is suggesting that you add more public methods to the medule classes,
As they currently have only the Meta class.
However, this warning can be safely ignored,
for form classes as they are not required to have public methods other than __init__ and clean.
"""
# pylint: disable=R0903

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, EmailValidator
from django.core.validators import MaxValueValidator, MinValueValidator


class RecipeManager(models.Manager):
    """Recipe manager for app"""
    def get_queryset(self):
        """
        Custom query set
        """
        return super().get_queryset()


class RecipeRatingManager(models.Manager):
    """Custom manager for RecipeRating model"""
    def avg_rating(self, recipe):
        """Calculates the average rating for a given recipe"""
        ratings = self.filter(recipe=recipe)
        if ratings:
            return sum([r.rating for r in ratings]) / len(ratings)
        return 0.0


class Recipe(models.Model):
    """Recipe Model for app"""
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    steps = models.TextField()
    ingredients = models.TextField()
    objects = RecipeManager()

    def __str__(self):
        return self.title

    def avg_rating(self):
        """Fucntion for calc avg rating"""
        ratings = RecipeRating.objects.filter(recipe=self)
        if ratings:
            return "{:.1f}".format(sum([r.rating for r in ratings]) / len(ratings))
        return "0.0"


class UserProfile(models.Model):
    """Class for UserProfile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(validators=[EmailValidator()])
    phone_number = models.CharField(
        validators=[MinLengthValidator(10)],
        max_length=20,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


class RecipeRating(models.Model):
    """Class for RecipeRating"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    objects = RecipeRatingManager()

    class Meta:
        """Meta Class for RecipeRating"""
        unique_together = ('recipe', 'user')

    def __str__(self):
        return f"{self.recipe.title} - {self.user.username}: {self.rating}"
