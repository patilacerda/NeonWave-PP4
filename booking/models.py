from django.db import models
from training.models import Activity

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