from django.db import models
from django.contrib.auth import get_user_model
from training.models import Activity

User = get_user_model()


# Create your models here.
class TimeAvailable(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    day = models.DateField()
    time = models.TimeField()

    class Meta:
        unique_together = ('activity', 'day', 'time')
        verbose_name = "Time Available"
        verbose_name_plural = "Times Available"

    def __str__(self):
        return f"{self.activity.name} - {self.day} at {self.time.strftime('%H:%M')}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_available = models.ForeignKey('TimeAvailable', on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.activity.name} - {self.day.strftime('%Y-%m-%d')} at {self.time.strftime('%H:%M')}"