from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from . import movieactions as ma
import requests
import json
import secrets

api_key = secrets.my_api_key()

def index(request):
    #index serves the view for a SINGLE movie/tvshow
    if request.GET:
        query_list = request.GET.getlist('q')
        if len( query_list ) > 1:
            url = "/movies/multi/?q=" + str(request.GET.getlist('q')[0]) + "&q=" + str(request.GET.getlist('q')[1])
            return redirect(url)

        id, media_type = query_list[0].split(",")
        project = ma.Project( requests.get("https://api.themoviedb.org/3/" + media_type + "/" + id + "?api_key=" + api_key + "&append_to_response=credits").json(), media_type )
        cast_crew = ma.cast_crew(project)

        singledict = {
            'project' : project,
            'cast_crew' : cast_crew,
        }

        return render(request,"movies/index.html",context=singledict)

    else:
        raise Http404

def multi(request):
    if request.GET:
        query_list = request.GET.getlist('q')
        if len(query_list) == 1 or query_list[0] == query_list[1]:
            # sends non-comparitive requests to the single view
            url = "/movies/?q=" + str(request.GET.getlist('q')[0])
            return redirect(url)

        project_list = []
        for query in query_list:
            id, media_type = query.split(",")
            project_list.append( ma.Project( requests.get("https://api.themoviedb.org/3/" + media_type + "/" + id + "?api_key=" + api_key + "&append_to_response=credits").json(), media_type ) )

        cast_crew = ma.cast_crew(*project_list)

        multidict = {
            'project_one' : project_list[0],
            'project_one_single' : "movies/?q=" + str(project_list[0].id) + "," + project_list[0].media_type,
            'project_two' : project_list[1],
            'project_two_single' : "movies/?q=" + str(project_list[1].id) + "," + project_list[1].media_type,
            'common_list' : cast_crew,
        }

        return render(request,"movies/multi.html",context=multidict)

    else:
        raise Http404
