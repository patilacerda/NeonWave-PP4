from django.urls import path
from . import views
from .views import BookingListView, book_class

urlpatterns = [
    path('booking/', views.BookingListView.as_view(), name='booking'),
    path('book/', book_class, name='book_class'),
    path(
        'cancel-booking/<int:booking_id>/',
        views.cancel_booking, name='cancel_booking'
        ),
]
