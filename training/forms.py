from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    A form class for creating or updating comments.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the CommentForm instance.
        Modifies the label of the 'body' field to False,
        removing it from the rendered form.
        """
        super().__init__(*args, **kwargs)
        self.fields['body'].label = False

    class Meta:
        model = Comment
        fields = ('body',)