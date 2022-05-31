from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('search/<query>/page/<page_number>', views.pagination, name='pagination'),
    path('game/<game_id>', views.game_details, name='game_details'),
    path('game/<game_id>/addgametoplay', views.add_to_play, name='add_toplay'),
    path('game/<game_id>/removegametoplay', views.remove_to_play, name='remove_toplay'),
    path('game/<game_id>/addgametoplayed', views.add_to_played, name='add_toplayed'),
    path('game/<game_id>/removegameplayed', views.remove_played, name='remove_played'),
    path('game/<game_id>/rate', views.rateGame, name='rate'),
    path('game/<game_id>/review/<username>', views.view_review, name='view_review'),
    path('game/<game_id>/review/<username>/delete', views.delete_review, name='delete_review')
]
