from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    """
    Used to update User related information, in this case
    the username.
    """
    class Meta:
        """
        Attaches the user related fields to the User model
        """
        model = User
        fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
    """
    Used to update Profile related information, in this case
    the profile picture, first name, last name, bio and
    location.
    """
    class Meta:
        """
        Attaches the profile related fields to the Profile model
        """
        model = Profile
        fields = [
            'profile_image', 'first_name', 'last_name', 'bio', 'location']
