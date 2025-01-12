from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput

from .models import Profile, Task


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Override the __init__ method to set the widget of date_due field
        to a DateInput widget with the "date" type and a placeholder of
        "yyyy-mm-dd". The widget is also given a class of "form-control".
        """
        super().__init__(*args, **kwargs)
        self.fields['date_due'].widget = forms.widgets.DateInput(
            attrs={
                "type": "date", "placeholder": "yyyy-mm-dd",
                "class": 'form-control'
            }
        )

    class Meta:
        model = Task
        fields = ["title", "content", "date_due"]


class UpdateTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Override the __init__ method to set the widget of date_completed field
        to a DateInput widget with the "date" type and a placeholder of
        "yyyy-mm-dd". The widget is also given a class of "form-control".
        """
        super().__init__(*args, **kwargs)
        self.fields['date_completed'].widget = forms.widgets.DateInput(
            attrs={
                "type": "date", "placeholder": "yyyy-mm-dd",
                "class": 'form-control'
            }
        )

    class Meta:
        model = Task
        fields = ["title", "content", "is_completed", "date_completed"]


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

    class Meta:
        model = User
        fields = ["username", "password"]


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "avatar",
            "email",
            "phone",
            "bio",
            "favorite_quote",
            "quote_author",
            "quote_source",
            "social_facebook",
            "social_linkedin",
            "social_github"
            ]
