from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Available"))

# Create your models here.
class Activity(models.Model):
    """
    Stores a single Activity available entry
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    duration = models.DurationField(default='45 minutes')
    status = models.IntegerField(choices=STATUS, default=0)


    def __str__(self):
        return self.name