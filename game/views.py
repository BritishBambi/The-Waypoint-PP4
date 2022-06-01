import os
from django.shortcuts import render, reverse, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth.models import User
import requests

from profiles.models import Profile
from .models import Game, Review

from .forms import RateForm

API_KEY = os.environ.get("API_KEY")


def home(request):
    """
    A simple function to render the home screen for the site

    """
    return render(request, 'index.html')


def search(request):
    """
    Takes a search query from the search bar and makes a call
    to the API for the game requested the game data for the query
    is then rendered into the search_results page

    """
    query = request.GET.get('query')

    if query:
        url = ('https://rawg.io/api/games?key=' + API_KEY +
               '&search=' + query +
               '&search_exact=1&ordering=-metacritic&page_size=12'
               )
        response = requests.get(url)
        game_data = response.json()

        context = {
            'query': query,
            'game_data': game_data,
            'page_number': 2,
        }

        template = loader.get_template('game/search_results.html')

        return HttpResponse(template.render(context, request))

    return render(request, 'game/search.html')


def pagination(request, query, page_number):
    """
    Renders the existing query again but adds the page_number variable on top
    this allows more results to be displayed onto the results page

    """
    url = ('https://rawg.io/api/games?key=' + API_KEY +
           '&search=' + query +
           '&search_exact=1&ordering=-metacritic&page_size=12&page=' +
           str(page_number)
           )
    response = requests.get(url)
    game_data = response.json()
    page_number = int(page_number) + 1

    context = {
            'query': query,
            'game_data': game_data,
            'page_number': page_number,
        }

    template = loader.get_template('game/search_results.html')

    return HttpResponse(template.render(context, request))


@login_required
def game_details(request, game_id):
    """
    Makes a API request with the game_id imported from the
    search results page, will then save the game name and api
    ID to the database for reference later. Will make checks
    against the game existing already in profile lists to ensure
    correct buttons are displayed on user view.

    """
    url = 'https://rawg.io/api/games/' + game_id + '?key=' + API_KEY
    response = requests.get(url)
    game_data = response.json()

    Game.objects.get_or_create(
            name=game_data['name'],
            gameID=game_data['id']
        )

    platforms = game_data['platforms']
    genres = game_data['genres']
    developers = game_data['developers']

    game = Game.objects.get(gameID=game_id)
    reviews = Review.objects.filter(game=game)
    reviews_avg = reviews.aggregate(Avg('rate'))
    reviews_count = reviews.count()
    user = request.user
    profile = Profile.objects.get(user=user)

    if profile.to_play.filter(gameID=game_id).exists():
        to_play = True
    else:
        to_play = False

    if profile.played.filter(gameID=game_id).exists():
        played = True
    else:
        played = False

    if Review.objects.filter(game=game, user=user).exists():
        review_exists = True
    else:
        review_exists = False

    context = {
        'game_data': game_data,
        'platforms': platforms,
        'genres': genres,
        'developers': developers,
        'reviews': reviews,
        'reviews_avg': reviews_avg,
        'reviews_count': reviews_count,
        'review_exists': review_exists,
        'to_play': to_play,
        'played': played
    }

    template = loader.get_template('game/game_details.html')

    return HttpResponse(template.render(context, request))


@login_required
def add_to_play(request, game_id):
    """
    Button to add the game to the to_play profile list
    and redirect back to the game page. Will only display
    if the game already doesnt exist in the list.

    """
    game = Game.objects.get(gameID=game_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    profile.to_play.add(game)
    messages.success(request, 'Game has been added to list')

    return HttpResponseRedirect(reverse('game_details', args=[game_id]))


@login_required
def remove_to_play(request, game_id):
    """
    Button to remove the game from the to_play profile list and
    redirect back to the game page. Will only display if the game
    already exists in the list.

    """
    game = Game.objects.get(gameID=game_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    profile.to_play.remove(game)
    messages.success(request, 'Game has been removed from list')

    return HttpResponseRedirect(reverse('game_details', args=[game_id]))


@login_required()
def add_to_played(request, game_id):
    """
    Button to add the game to the played profile list and redirect
    back to the game page. Will only display if the game already
    doesnt exist in the list.

    """
    game = Game.objects.get(gameID=game_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    if profile.to_play.filter(gameID=game_id).exists():
        profile.to_play.remove(game)
        profile.played.add(game)
    else:
        profile.played.add(game)

    messages.success(request, 'Game has been added to list')

    return HttpResponseRedirect(reverse('game_details', args=[game_id]))


@login_required
def remove_played(request, game_id):
    """
    Button to remove the game from the played profile list and
    redirect back to the game page. Will only display if the game
    already exists in the list.

    """
    game = Game.objects.get(gameID=game_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    profile.played.remove(game)
    messages.success(request, 'Game has been removed from list')

    return HttpResponseRedirect(reverse('game_details', args=[game_id]))


@login_required
def rateGame(request, game_id):
    """
    Checks for a valid POST request from the rate/review page
    and saves the score and review to the Review model. Checks
    for an existing review to make sure the user cannot post
    multiple. Will also remove the game from any proifle lists
    that are applicable.

    """
    game = Game.objects.get(gameID=game_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    if Review.objects.filter(game=game, user=user).exists():
        review_exists = True
    else:
        review_exists = False

    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = user
            rate.game = game
            profile.to_play.remove(game)
            profile.played.add(game)
            rate.save()
            messages.success(request, 'Review saved')

            return HttpResponseRedirect(
                reverse('game_details', args=[game_id])
                )

    else:
        form = RateForm()

    template = loader.get_template('game/rate.html')

    context = {
        'form': form,
        'game': game,
        'review_exists': review_exists
    }

    return HttpResponse(template.render(context, request))


def view_review(request, username, game_id):
    """
    A simple function to render an existing review with the context of
    the review itself and the game that was reviewed.

    """
    user = get_object_or_404(User, username=username)
    game = Game.objects.get(gameID=game_id)
    review = Review.objects.get(user=user, game=game)

    context = {
        'review': review,
        'game': game,
    }

    template = loader.get_template('game/review.html')

    return HttpResponse(template.render(context, request))


@login_required()
def delete_review(request, username, game_id):
    """
    Checks for a valid POST request from the delete_review page
    to simply delete the exisitng review model. The user will then
    be returned to the game page.

    """
    user = get_object_or_404(User, username=username)
    game = Game.objects.get(gameID=game_id)
    review = Review.objects.get(user=user, game=game)

    if request.method == 'POST':
        review.delete()
        return HttpResponseRedirect(reverse('game_details', args=[game_id]))

    context = {
        'review': review,
        'game': game,
    }

    return render(request, 'game/delete_review.html', context)
