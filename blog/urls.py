from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.posts, name='posts'),
    url(r'^posts$', views.posts, name='posts'),
    url(r'^blogs$', views.blogs, name='blogs'),
    url(r'^people$', views.people, name='people'),
    url(r'^about$', views.about, name='about'),
]
