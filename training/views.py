from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import Activity, Comment
from .forms import CommentForm

# Create your views here.
class ActivityList(generic.ListView):
    queryset = Activity.objects.all()
    template_name = "activity_list.html"

def activity_comment(request, slug):
    activity = get_object_or_404(Activity, slug=slug, status=1)
    comments = activity.comments.all()
    comment_count = activity.comments.filter(approved=True).count()
    comment_form = CommentForm()
    
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.activity = activity
            comment.save()
            messages.add_message(
            request, messages.SUCCESS,
            'Comment submitted and awaiting approval'
            )

    return render(
    request,
    "activity_list.html",
    {
        "object_list": [activity],
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
    },
    )