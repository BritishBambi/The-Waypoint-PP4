from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

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
        }

        template = loader.get_template('search_results.html')

        return HttpResponse(template.render(context, request))

    return render(request, 'search.html')
