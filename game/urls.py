from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('search/<query>/page/<page_number>', views.pagination, name='pagination'),
    path('game/', views.game_details, name='game'),
]
