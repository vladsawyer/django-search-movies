from django import forms
from movies.models import Comments


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ("text", "image", "user")
