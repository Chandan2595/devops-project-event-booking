"""Django models here"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    """Event class"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    max_participants = models.IntegerField(default=5)
    num_participants = models.IntegerField(default=0)

    def __str__(self):
        return str(self.title)


class Participant(models.Model):
    """Participent class"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    events = models.ManyToManyField(Event, related_name="participants")

    def __str__(self):
        return str(self.name)
        