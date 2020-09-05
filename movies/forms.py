from django import forms
from movies.models import Comments, Likes


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ("text", "image", "user")


class LikeForm(forms.ModelForm):
    class Meta:
        model = Likes
        fields = ("user", "value")
