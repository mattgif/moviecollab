from django.conf.urls import url
from people import views

app_name = 'people'

urlpatterns = [
	url(r'^$',views.find_common,name='peopleindex'),    
    url(r'profile/',views.profile,name='profile'),
]
