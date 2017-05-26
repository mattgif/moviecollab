from django.conf.urls import url
from movies import views

app_name = "movies"

urlpatterns = [
	url(r'^$',views.index,name='movieindex'),
    url(r'multi/',views.multi,name="moviemulti")
]
