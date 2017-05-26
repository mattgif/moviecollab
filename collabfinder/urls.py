from django.conf.urls import url
from . import views

app_name = 'collabfinder'

urlpatterns = [
    url(r'^$',views.index,name="index"),
    url(r'^movies/',views.movie_search,name="movies_search"),
    url(r'^people/',views.people_search,name="people_search"),
]
