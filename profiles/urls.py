from django.urls import path
from . import views

urlpatterns = [
    path('<username>', views.profile, name='profile'),
    path('<username>/edit/', views.edit_profile, name='editProfile'),
    path('<username>/delete', views.delete_profile, name='deleteProfile')
]
