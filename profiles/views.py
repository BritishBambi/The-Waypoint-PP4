from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def editProfile(request):
    return render(request, 'edit_profile.html')
