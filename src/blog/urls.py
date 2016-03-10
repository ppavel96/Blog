from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/posts/hot/', permanent=True)),
    url(r'^posts/$', RedirectView.as_view(url='/posts/hot/', permanent=True)),
    url(r'^posts/(hot|new|best|feed)/$', views.posts, name='posts'),

    url(r'^blogs/$', RedirectView.as_view(url='/blogs/popular/', permanent=True)),
    url(r'^blogs/(popular|new|feed)/$', views.blogs, name='blogs'),

    url(r'^people/$', views.people, name='people'),
    url(r'^about/$', views.about, name='about'),

    url(r'^ajax/posts/$', views.ajax_posts, name='ajax_posts'),

    url(r'^robots.txt$', TemplateView.as_view(template_name='blog/robots.txt', content_type='text/plain')),
    url(r'^humans.txt$', TemplateView.as_view(template_name='blog/humans.txt', content_type='text/plain')),

    url(r'^(?!admin$).*/$', views.page_404, name='page_404'),
]
