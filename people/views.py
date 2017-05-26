from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
import requests
import json
from . import peopleactions as pa
import secrets

api_key = secrets.my_api_key()

def find_common( request ):
    if request.GET:
        query_list = request.GET.getlist('q')

        if len( query_list ) == 1 or query_list[0] == query_list[1]:
            url = "/people/profile/?q=" + str(request.GET.getlist('q')[0])
            return redirect(url)

        l = [requests.get("https://api.themoviedb.org/3/person/" + id + "?api_key=" + api_key + "&append_to_response=combined_credits").json() for id in query_list]
        hero = pa.Person(l[0])
        collab = pa.Person(l[1])

        common_list = pa.find_common_projects(hero,collab)

        collab_dict = {
            'name':hero.name,
            'hero':hero,
            'profile_image':hero.image_url('md'),
            'hero_id':hero.id,
            'hero_profile': "/people/profile/?q=" + str(hero.id),
            'collab_id' : collab.id,
            'collab_profile': "/people/profile/?q=" + str(collab.id),
            'collab_name' : collab.name,
            'collab': collab,
            'collab_image' : collab.image_url('md'),
            'common_list' : common_list}

        return render(request,"people/common.html",context=collab_dict)
    else:
        raise Http404

def profile(request):
    if request.GET:
        query_list = request.GET.getlist('q')
        if len( query_list ) > 1:
            url = "/people/?q=" + str(request.GET.getlist('q')[0]) + "&q=" + str(request.GET.getlist('q')[1])
            return redirect(url)

        hero = pa.Person( requests.get("https://api.themoviedb.org/3/person/" + query_list[0] + "?api_key=" + api_key + "&append_to_response=combined_credits").json() )

        common_list = pa.find_common_projects(hero,hero)

        profile_dict = {
            'name':hero.name,
            'hero':hero,
            'profile_image':hero.image_url('md'),
            'hero_id':hero.id,
            'common_list':common_list,
            }

        return render(request,"people/profile.html",context=profile_dict)
    else:
        raise Http404
