import os
from django.test import TestCase
from django.contrib.auth import get_user_model
import requests
from profiles.models import Profile
from .models import Game, Review
from .forms import RateForm 

API_KEY = os.environ.get("API_KEY")

# Create your tests here.


class TestViews(TestCase):
    """
    Testing for game views

    Test Case = TC

    TC1 - Test Home/Index
    TC2 - Test Search Page
    TC3 - Test Search Results Page
    TC4 - Test Pagination
    TC5 - Test Game Details Page
    TC6 - Test Add to play
    TC7 - Test Remove from Play
    TC8 - Test Add to played
    TC9 - Test Removed from played
    TC10 - Test Rate Page
    TC11 - Test Review Page
    """
    def setUp(self):
        """ Create test login user and create Profile entry"""
        username = "jojo"
        pswd = "Trials"
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username=username,
                                                   password=pswd,
                                                   is_superuser=True)
        logged_in = self.client.login(username=username, password=pswd)

        self.assertTrue(logged_in)

    def test_home_page(self):
        """ TC1 - Test home view renders correct page """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_search_page(self):
        """ TC2 - Test search view renders the correct page"""
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/search.html')

    def test_search_results(self):
        """ TC3 - Test search results page renders with game information """
        response = self.client.get('/search/?query=Halo&action=')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/search_results.html')

    def test_pagination(self):
        """ TC4 - Test pagination page works as intended """
        response = self.client.get('/search/Halo/page/2')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/search_results.html')

    def test_game_details(self):
        """ TC5 - Test game details page renders
        and new game entry into database is created as intended """
        response = self.client.get('/game/28589')

        url = 'https://rawg.io/api/games/28589?key=' + API_KEY
        api_response = requests.get(url)
        game_data = api_response.json()
        Game.objects.get_or_create(
            name=game_data['name'],
            gameID=game_data['id']
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/game_details.html')
        self.assertTrue(Game.objects.get(gameID="28589"))

    def test_add_to_play(self):
        """ TC6 - Test games are added to to_play list """
        user = self.user
        url = 'https://rawg.io/api/games/28589?key=' + API_KEY
        api_response = requests.get(url)
        game_data = api_response.json()
        Game.objects.get_or_create(
            name=game_data['name'],
            gameID=game_data['id']
        )

        game = Game.objects.get(gameID="28589")
        profile = Profile.objects.get(user=user)
        profile.to_play.add(game)
        response = self.client.get('/game/28589/addgametoplay')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(profile.to_play.filter(gameID="28589"))

    def test_remove_to_play(self):
        """ TC7 - Test games are removed from to_play list """
        user = self.user
        url = 'https://rawg.io/api/games/28589?key=' + API_KEY
        api_response = requests.get(url)
        game_data = api_response.json()
        Game.objects.get_or_create(
            name=game_data['name'],
            gameID=game_data['id']
        )

        game = Game.objects.get(gameID="28589")
        profile = Profile.objects.get(user=user)
        profile.to_play.add(game)
        profile.to_play.remove(game)
        response = self.client.get('/game/28589/removegametoplay')

        self.assertEqual(response.status_code, 302)
        self.assertFalse(profile.to_play.filter(gameID="28589"))

    def test_add_to_played(self):
        """ TC8 - Test games are added to played list """
        user = self.user
        url = 'https://rawg.io/api/games/28589?key=' + API_KEY
        api_response = requests.get(url)
        game_data = api_response.json()
        Game.objects.get_or_create(
            name=game_data['name'],
            gameID=game_data['id']
        )

        game = Game.objects.get(gameID="28589")
        profile = Profile.objects.get(user=user)
        profile.played.add(game)
        response = self.client.get('/game/28589/addgametoplayed')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(profile.played.filter(gameID="28589"))

    def test_remove_played(self):
        """ TC9 - Test games are removed from played list """
        user = self.user
        url = 'https://rawg.io/api/games/28589?key=' + API_KEY
        api_response = requests.get(url)
        game_data = api_response.json()
        Game.objects.get_or_create(
            name=game_data['name'],
            gameID=game_data['id']
        )

        game = Game.objects.get(gameID="28589")
        profile = Profile.objects.get(user=user)
        profile.played.add(game)
        profile.played.remove(game)
        response = self.client.get('/game/28589/removegameplayed')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(profile.played.filter(gameID="28589"))

    def test_rate_page(self):
        """ TC10 - Test reviews can be saved and retrieved """
        url = 'https://rawg.io/api/games/28589?key=' + API_KEY
        api_response = requests.get(url)
        game_data = api_response.json()
        user = self.user
        Game.objects.get_or_create(
            name=game_data['name'],
            gameID=game_data['id']
        )
        game = Game.objects.get(gameID="28589")

        Review.objects.get_or_create(
            user=self.user,
            game=game,
            rate='3'
        )

        review = Review.objects.get(user=user, game=game)

        response = self.client.post('/game/28589/rate')
        self.assertTemplateUsed(response, 'game/rate.html')
        self.assertTrue(review.game.gameID=="28589")

    def test_review_page(self):
        """ TC11 - Test reviews can be rendered on their own page """
        url = 'https://rawg.io/api/games/28589?key=' + API_KEY
        api_response = requests.get(url)
        game_data = api_response.json()
        user = self.user
        Game.objects.get_or_create(
            name=game_data['name'],
            gameID=game_data['id']
        )
        game = Game.objects.get(gameID="28589")

        Review.objects.get_or_create(
            user=self.user,
            game=game,
            rate='3'
        )

        review = Review.objects.get(user=user, game=game)

        response = self.client.post('/game/28589/review/jojo')
        self.assertTemplateUsed(response, 'game/review.html')
        self.assertTrue(review.game.gameID == "28589")
