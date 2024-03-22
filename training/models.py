from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Available"))

# Create your models here.
class Activity(models.Model):
    """
    Stores a single Activity available entry
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    duration = models.DurationField()
    status = models.IntegerField(choices=STATUS, default=0)
    max_capacity = models.PositiveIntegerField(default=10)
    featured_image = CloudinaryField('image', default='placeholder')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name