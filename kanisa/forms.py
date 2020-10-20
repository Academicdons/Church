from django.contrib.auth.models import User
from django import forms

from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = blogComment
        fields = ('name', 'email', 'body')
