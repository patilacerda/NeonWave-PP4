from django.shortcuts import render
from django.views import generic
from .models import Activity

# Create your views here.
class ActivityList(generic.ListView):
    queryset = Activity.objects.all()
    template_name = "activity_list.html"
