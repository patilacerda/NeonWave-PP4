from . import views
from django.urls import path

urlpatterns = [
    path('', views.ActivityList.as_view(), name='home'),
    path('comments/<slug>', views.activity_comment, name='activity_comments'),
    path('comments/<slug>/edit_comment/<int:comment_id>',
         views.comment_edit, name='comment_edit'),
]