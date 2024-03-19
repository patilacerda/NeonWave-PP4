from . import views
from django.urls import path

urlpatterns = [
    path('', views.ActivityList.as_view(), name='Classes'),
]