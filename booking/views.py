from django.shortcuts import render
from django.views import generic
from .models import TimeAvailable

# Create your views here.
class BookingListView(generic.ListView):
    queryset = TimeAvailable.objects.all()
    template_name = 'booking.html'
    context_object_name = 'classes_available'
    paginate_by = 6