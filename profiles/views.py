from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Profile

from .forms import UserUpdateForm, ProfileUpdateForm

# Create your views here.


def profile(request, username):
    """
    Renders the user profile for the related username in the url,
    this ensures any profle can be viewed by loading the template
    and certain permissions can be requested in the template.

    """
    user = get_object_or_404(User, username=username)
    user_profile = Profile.objects.get(user=user)

    context = {
        'profile': user_profile,
    }

    template = loader.get_template('profiles/profile.html')

    return HttpResponse(template.render(context, request))


@login_required
def edit_profile(request, username):
    """
    Renders the user and profile update form to the edit_profile page
    and checks for a valid POST request to save the form information
    to the database.

    """
    user = get_object_or_404(User, username=username)
    user_profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
            )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect(reverse('home'))
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': user_profile
    }
    return render(request, 'profiles/edit_profile.html', context)


def delete_profile(request, username):
    """
    Checks for a valid post request to allow the user to
    delete their own user account. Ensures this can only be
    done by the correct user within the template.

    """
    user = get_object_or_404(User, username=username)
    user_profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted!')
        return redirect(reverse('home'))

    context = {
        'profile': user_profile
    }

    return render(request, 'profiles/delete_profile.html', context)
