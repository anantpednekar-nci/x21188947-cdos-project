"""
Module for forms related to the recipes app.

R0903: Too few public methods (0/2) (too-few-public-methods)
These warnings are related to the number of public methods in the form classes.
A public method is a method that can be accessed outside of the class.
The linter is suggesting that you add more public methods to the form classes,
As they currently have only the Meta class.
However, this warning can be safely ignored for form classes,
as they are not required to have public methods other than __init__ and clean.
"""
# pylint: disable=R0903

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, EmailValidator
from .models import Recipe

HELP_TEXT = "optional"


class RecipeForm(forms.ModelForm):
    """Form for creating and updating a recipe."""
    title = forms.CharField(validators=[MinLengthValidator(3)])

    class Meta:
        """Meta Class for RecipeRating"""
        model = Recipe
        fields = ('title', 'description', 'image', 'steps', 'ingredients')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'steps': forms.Textarea(attrs={'class': 'form-control'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control'}),
        }


class RegistrationForm(UserCreationForm):
    """Form for user registration."""
    email = forms.EmailField(required=True, validators=[EmailValidator()])
    first_name = forms.CharField(max_length=30, required=False, help_text=HELP_TEXT)
    last_name = forms.CharField(max_length=30, required=False, help_text=HELP_TEXT)

    class Meta:
        """Meta class  for user registration."""
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data



class UpdateProfileForm(forms.ModelForm):
    """Form for updating user profile information."""
    first_name = forms.CharField(max_length=30, required=False, help_text=HELP_TEXT)
    last_name = forms.CharField(max_length=30, required=False, help_text=HELP_TEXT)
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        """Meta class for updating user profile information."""
        model = User
        fields = ('first_name', 'last_name', 'email')


class RecipeRatingForm(forms.Form):
    """Form for rating a recipe."""
    rating = forms.ChoiceField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                               widget=forms.Select(attrs={'class': 'form-control'}))
