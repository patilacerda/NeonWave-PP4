from django.db import models
from django.contrib.auth import get_user_model
from training.models import Activity

User = get_user_model()


# Create your models here.
class TimeAvailable(models.Model):
    """
    Model representing the available times for activities.
    Stores information about the availability of time slots for activities.
    Attributes:
        activity (ForeignKey): The activity associated with the available time.
        day (DateField): The date of the available time slot.
        time (TimeField): The time of the available time slot.
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    day = models.DateField()
    time = models.TimeField()

    class Meta:
        unique_together = ('activity', 'day', 'time')
        verbose_name = "Time Available"
        verbose_name_plural = "Times Available"

    def __str__(self):
        return f"""
        {self.activity.name} -{self.day} at {self.time.strftime('%H:%M')}"""


class Booking(models.Model):
    """
    Model representing a booking made by a user.
    Attributes:
        user (ForeignKey): The user who made the booking.
        time_available (ForeignKey): The time available for booking.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_available = models.ForeignKey(
        'TimeAvailable', on_delete=models.CASCADE)

    def __str__(self):
        return f"""{self.activity.name} - {self.day.strftime('%Y-%m-%d')}
        at {self.time.strftime('%H:%M')}"""