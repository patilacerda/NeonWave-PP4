from django.urls import path
from . import views
from .views import BookingListView

urlpatterns = [
    path('booking/', views.BookingListView.as_view(), name='booking'),
]