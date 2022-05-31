from django.urls import path
from . import views

urlpatterns = [
    path('<username>', views.profile, name='profile'),
    path('<username>/edit/', views.editProfile, name='editProfile'),
    path('<username>/delete', views.deleteProfile, name='deleteProfile')
]
