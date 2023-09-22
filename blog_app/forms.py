from django.forms import ModelForm
from .models import Comment


class CommentForm(ModelForm):
    """ Comment form for taking comment input from user and validate and save to database """
    class Meta:
        """ Metadata """
        model = Comment
        fields = ['name', 'email', 'message', 'post']
