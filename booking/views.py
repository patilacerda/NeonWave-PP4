from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from .models import TimeAvailable, Booking
from .forms import BookingForm

class BookingListView(generic.ListView):
    queryset = TimeAvailable.objects.all()
    template_name = 'booking.html'
    context_object_name = 'classes_available'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booked_classes'] = Booking.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = BookingForm(request.POST)
        if form.is_valid():
            selected_class_id = form.cleaned_data['selected_class_id']
            time_available = TimeAvailable.objects.get(pk=selected_class_id)
            
            # Create a booking object
            booking = Booking.objects.create(user=request.user, time_available=time_available)

            return HttpResponseRedirect(request.path_info)  # Redirect to the same page
        else:

            return self.get(request, *args, **kwargs)

def book_class(request):
    if request.method == 'POST':

        return HttpResponseRedirect(reverse('booking'))
    else:
        return HttpResponseRedirect(reverse('booking'))