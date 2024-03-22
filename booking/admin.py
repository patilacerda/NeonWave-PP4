from django.contrib import admin
from django.db import models
from django.forms import Select
from datetime import timedelta
from .models import TimeAvailable
from training.models import Activity

# Register your models here.
@admin.register(TimeAvailable)
class TimeAvailableAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TimeField: {
            'widget': Select(choices=[
            ('08:00:00', '08:00 AM'),
            ('09:00:00', '09:00 AM'),
            ('10:00:00', '10:00 AM'),
            ('15:00:00', '03:00 PM'),
            ('16:00:00', '04:00 PM'),
            ('17:00:00', '05:00 PM'),
        ])},
    }

    list_display = ['activity', 'day', 'time', 'remaining_slots']
    list_filter = ['activity', 'day', 'time']

    def remaining_slots(self, obj):
        """
        Calculate and display the remaining slots for each time slot.
        """
        total_slots = obj.booking_set.count()
        max_slots = obj.activity.max_capacity
        remaining = max_slots - total_slots
        return max(remaining, 0)

    remaining_slots.short_description = 'Remaining Slots'