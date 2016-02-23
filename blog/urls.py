from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.posts, name='posts'),
    url(r'^posts/?$', views.posts, name='posts'),
    url(r'^posts/(hot|new|best|feed)$', views.posts, name='posts'),

    url(r'^blogs$', views.blogs, name='blogs'),
    url(r'^people$', views.people, name='people'),
    url(r'^about$', views.about, name='about'),

    url(r'^robots.txt$', TemplateView.as_view(template_name='blog/robots.txt', content_type='text/plain')),
    url(r'^humans.txt$', TemplateView.as_view(template_name='blog/humans.txt', content_type='text/plain')),

    url(r'^(?!admin$).*', views.page_404, name='page_404'),
]
