from django.db import models

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=30)
    description = models.TextField()
    ingredients = models.JSONField()
    steps = models.JSONField()
    image = models.ImageField()
    
    def __str__(self):
        return self.title

'''

class Rating(models.Model):
    movie = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    '''