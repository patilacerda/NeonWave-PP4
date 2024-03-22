from django.db import models
from django.db.models import Count, F
from django.contrib import messages
from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from .models import TimeAvailable, Booking
from training.models import Activity
from .forms import BookingForm


class BookingListView(generic.ListView):
    """
    Retrieves the list of time slots available for booking from the database
    and sends them to the template
    """
    template_name = 'booking.html'
    context_object_name = 'classes_available'
    paginate_by = 6

    def get_queryset(self):
        # Get all TimeAvailable objects
        queryset = TimeAvailable.objects.all()
        # Filter out classes that have reached maximum capacity
        queryset = queryset.annotate(num_bookings=Count('booking'))
        queryset = queryset.filter(num_bookings__lt=models.F('activity__max_capacity'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booked_classes'] = Booking.objects.filter(
            user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = BookingForm(request.POST)
        if form.is_valid():
            # Check if user has reached the booking limit
            if Booking.objects.filter(user=request.user).count() >= 6:
                messages.error(request, "You have reached the maximum number of bookings. Please cancel a class or wait until your next session is completed.")
                return redirect('booking')
            
            selected_class_id = form.cleaned_data['selected_class_id']
            time_available = TimeAvailable.objects.get(pk=selected_class_id)
            
            # Create a booking object
            booking = Booking.objects.create(
                user=request.user, time_available=time_available)

            return HttpResponseRedirect(request.path_info)
        else:

            return self.get(request, *args, **kwargs)


def book_class(request):
    """
    This function handles the HTTP POST request for booking a class.
    """
    if request.method == 'POST':

        return HttpResponseRedirect(reverse('booking'))
    else:
        return HttpResponseRedirect(reverse('booking'))


def cancel_booking(request, booking_id):
    """
    This function cancels a booking based on the provided booking_id.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    # Check if the user owns the booking or has permission to cancel it
    if request.user == booking.user:
        booking.delete()
        return redirect('booking')
    else:
        # Handle unauthorized cancellation attempt
        return redirect('booking')
