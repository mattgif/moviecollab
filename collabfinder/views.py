from django.shortcuts import render
from django.http import HttpResponse
import requests
import secrets

api_key = secrets.my_api_key()

# Create your views here.
def index(request):
    return render(request,"collabfinder/index.html")
