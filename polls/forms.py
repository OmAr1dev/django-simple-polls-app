from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Choice, Poll


class RegisterForm(UserCreationForm):
    """
    Form for registering a new user.
    Extends Django's UserCreationForm and adds an email field.
    """

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PollCreateForm(forms.ModelForm):
    """Form to create a poll with dynamic number of choices."""

    num_choices = forms.IntegerField(
        label="Number of Choices", min_value=2, max_value=10, initial=2
    )

    class Meta:
        model = Poll
        fields = ["title"]


# class PollForm(forms.ModelForm):
#     """
#     Form for creating a new poll.
#     The creator is set in the view, not in the form.
#     """

#     class Meta:
#         model = Poll
#         fields = ["title"]
#         labels = {"title": "Poll Title"}


# class ChoiceForm(forms.ModelForm):
#     """
#     Form for creating a new choice for a poll.
#     """

#     class Meta:
#         model = Choice
#         fields = ["text"]
#         labels = {"text": "Choice Text"}


# class PollChoicesNumberForm(forms.Form):
#     """
#     Form to choose how many choices a new poll will have.
#     """

#     num_choices = forms.IntegerField(
#         label="Number of Choices", min_value=2, max_value=10, initial=2
#     )
