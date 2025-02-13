from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()

class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Participant(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    event = models.ManyToManyField(Event)