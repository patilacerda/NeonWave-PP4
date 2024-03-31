from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Activity, Comment
from .forms import CommentForm


# Create your views here.
class ActivityList(generic.ListView):
    """
    Displays a list of all activities.
    """
    queryset = Activity.objects.all()
    template_name = "activity_list.html"


@login_required
def activity_comment(request, slug):
    """
    Handles comments on activities.
    Retrieves the activity based on the slug provided in the URL.
    If the request method is POST and the comment form is valid,
    it saves the comment associated with the activity.
    Redirects to the activity detail page after submitting the comment.
    """
    activity = get_object_or_404(Activity, slug=slug, status=1)
    comments = activity.comments.all()
    comment_count = activity.comments.filter(approved=True).count()

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
    comment_form = CommentForm()
    return render(
        request, "training/activity_detail.html", {
            "object_list": [activity],
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },
    )


def comment_edit(request, slug, comment_id):
    """
    Handles editing of comments.
    Retrieves the activity and comment objects based on the provided slugs
    and comment ID.
    Renders a form for editing the comment. If the request method is POST and
    the form is valid, it updates the comment and redirects to the activity
    detail page.
    """
    print("edit:", comment_id)
    queryset = Activity.objects.all()
    activity = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)
    comment_form = CommentForm(instance=comment)
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST, instance=comment)
        if comment_form.is_valid() and comment.user == request.user:
            comment = comment_form.save(commit=False)
            comment.activity = activity
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
            return HttpResponseRedirect(reverse(
                'activity_detail', args=[slug]))
        else:
            messages.add_message(
                request, messages.ERROR, 'Error updating comment!')
    else:
        return render(request, "training/edit_comment.html", {
            "activity": activity,
            "comment": comment,
            "comment_form": comment_form,
        },
        )


def comment_delete(request, slug, comment_id):
    """
    Handles deletion of comments.
    Retrieves the activity and comment objects based on the provided slugs and
    comment ID.
    Deletes the comment if the current user is the author. Otherwise, displays
    an error message.
    Redirects to the activity detail page after deletion.
    """
    queryset = Activity.objects.filter(status=1)
    activity = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.user == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(
            request, messages.ERROR, 'You can only delete your own comments!')
    return HttpResponseRedirect(reverse('activity_detail', args=[slug]))
