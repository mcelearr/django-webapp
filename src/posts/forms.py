from django import forms
from django.contrib.auth.models import User

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
        ]

class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField()
    last_name = forms.CharField()
    password=forms.CharField(max_length=30,widget=forms.PasswordInput())
    email=forms.EmailField(required=False)

    def clean_username(self): # check if username dos not exist before
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']

        raise forms.ValidationError("this user exist already")

    def save(self):
        new_user=User.objects.create_user(self.cleaned_data['username'],
                                          self.cleaned_data['email'],
                                          self.cleaned_data['password'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()
