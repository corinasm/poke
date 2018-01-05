from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login ),
    url(r'^logout$', views.logout ),
    url(r'^pokes$', views.pokes),
    url(r'^poke_user/(?P<user_id>\d+)$', views.poke_user),
]