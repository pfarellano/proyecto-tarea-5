from django.conf.urls import url
from paginatarea5 import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^episodio/?(?P<id>\d+)?/?$', views.episodio, name='episodio'),
    url(r'^episodio/$', views.episodio, name='episodio'),
    url(r'^personaje/?(?P<ur>\d+)?/?$', views.personaje, name='personaje'),
    url(r'^personaje/$', views.personaje, name='personaje'),
    url(r'^lugar/?(?P<id>\d+)?/?$', views.lugar, name='lugar'),
    url(r'^lugar/$', views.lugar, name='lugar'),
    url(r'^busqueda/$', views.busqueda, name='busqueda'),
]