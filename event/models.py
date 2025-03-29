from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    participants = models.ManyToManyField(User, related_name="events")
    asset = models.ImageField(upload_to="event_assets", null=True, blank=True, 
    default="event_assets/default1.png")

    def __str__(self):
        return self.name