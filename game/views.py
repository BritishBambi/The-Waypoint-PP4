from django.shortcuts import render, reverse, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Avg
from django.contrib.auth.models import User
from profiles.models import Profile
from .models import Game, Review


from .forms import RateForm

import requests


def home(request):
    return render(request, 'index.html')


def search(request):
    query = request.GET.get('query')

    if query:
        url = 'https://rawg.io/api/games?key=c4a730f92484414c82505dab317c1720&search=' + query + '&search_exact=1&ordering=-metacritic&page_size=12'
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
    url = 'https://rawg.io/api/games?key=c4a730f92484414c82505dab317c1720&search=' + query + '&search_exact=1&ordering=-metacritic&page_size=12&page=' + str(page_number)
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


def game_details(request, game_id):
    url = 'https://rawg.io/api/games/' + game_id + '?key=c4a730f92484414c82505dab317c1720'
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
    if Review.objects.filter(user=user).exists():
        review_exists = True

    context = {
        'game_data': game_data,
        'platforms': platforms,
        'genres': genres,
        'developers': developers,
        'reviews': reviews,
        'reviews_avg': reviews_avg,
        'reviews_count': reviews_count,
        'review_exists': review_exists
    }

    template = loader.get_template('game/game_details.html')

    return HttpResponse(template.render(context, request))


@login_required
def add_to_play(request, game_id):
    game = Game.objects.get(gameID=game_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    profile.to_play.add(game)
    messages.success(request, 'Game has been added to list')

    return HttpResponseRedirect(reverse('game_details', args=[game_id]))


@login_required
def remove_to_play(request, game_id):
    game = Game.objects.get(gameID=game_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    profile.to_play.remove(game)
    messages.success(request, 'Game has been removed from list')

    return HttpResponseRedirect(reverse('game_details', args=[game_id]))


@login_required()
def add_to_played(request, game_id):
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
    game = Game.objects.get(gameID=game_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    profile.played.remove(game)
    messages.success(request, 'Game has been removed from list')

    return HttpResponseRedirect(reverse('game_details', args=[game_id]))


@login_required
def rateGame(request, game_id):
    game = Game.objects.get(gameID=game_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    if Review.objects.filter(user=user).exists():
        review_exists = True

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

            return HttpResponseRedirect(reverse('game_details', args=[game_id]))

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
    user = get_object_or_404(User, username=username)
    game = Game.objects.get(gameID=game_id)
    review = Review.objects.get(user=user, game=game)

    context = {
        'review': review,
        'game': game,
    }

    template = loader.get_template('game/review.html')

    return HttpResponse(template.render(context, request))
