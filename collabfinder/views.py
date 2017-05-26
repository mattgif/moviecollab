from django.shortcuts import render
from django.http import HttpResponse
import tmdbsimple as tmdb
import requests
import secrets

api_key = secrets.my_api_key()
tmdb.API_KEY = api_key

# Create your views here.
def index(request):
    return render(request,"collabfinder/index.html")

# autocomplete for movies / tv
def movie_search( request ):
    if request.is_ajax():
        # check for ?q= in url, and passes that to tmdb
        term = request.GET.get("q")
        if len(term) > 2 and term is not None:
            api_response = requests.get('https://api.themoviedb.org/3/search/movie?api_key='+api_key+"&language=en-US&query="+term)
            # enable for debugging results:
            # print(api_response.json())
            return HttpResponse(api_response.text, content_type='application/json')

# autocomplete results for people
def people_search( request ):
    if request.is_ajax():
        term = request.GET.get("q")
        if len(term) > 2 and term is not None:
            api_response = requests.get('https://api.themoviedb.org/3/search/person?api_key='+api_key+"&language=en-US&query="+term)
            return HttpResponse(api_response.text, content_type='application/json')
