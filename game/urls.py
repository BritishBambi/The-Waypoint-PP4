from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('search/<query>/page/<page_number>', views.pagination, name='pagination'),
    path('game/<game_id>', views.game_details, name='game_details'),
    path('game/<game_id>/addgametoplay', views.add_to_play, name='add_toplay'),
    path('game/<game_id>/addgametoplayed', views.add_to_played, name='add_toplayed'),
]
