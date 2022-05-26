from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from .forms import UserUpdateForm, ProfileUpdateForm

# Create your views here.


def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = Profile.objects.get(user=user)

    context = {
    'profile': user_profile,
    }

    template = loader.get_template('profiles/profile.html')

    return HttpResponse(template.render(context, request))


@login_required
def editProfile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect(reverse('profile', args=[user]))
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': user_profile
    }
    return render(request, 'profiles/edit_profile.html', context)
