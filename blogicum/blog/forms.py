from django import forms

from .models import Comment, Post, User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'is_staff',
                             'is_active', 'is_superuser', 'date_joined',
                             'last_login', 'password')
