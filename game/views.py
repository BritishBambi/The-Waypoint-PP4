from django.shortcuts import render, reverse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from profiles.models import Profile


from .models import Game

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

    game = Game.objects.get_or_create(
            name=game_data['name'],
            gameID=game_data['id']
        )

    platforms = game_data['platforms']
    genres = game_data['genres']
    developers = game_data['developers']

    context = {
        'game_data': game_data,
        'platforms': platforms,
        'genres': genres,
        'developers': developers,
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
