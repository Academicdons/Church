from django.contrib.auth.models import User
from django import forms

from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = blogComment
        fields = ('name', 'email', 'body')


class SermonCommentForm(forms.ModelForm):
    class Meta:
        model = SermonsComment
        fields = ('name', 'email', 'body')


class EventsCommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ('name', 'email', 'body')
