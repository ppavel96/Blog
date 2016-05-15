from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/posts/hot/', permanent=True)),
    url(r'^posts/$', RedirectView.as_view(url='/posts/hot/', permanent=True)),
    url(r'^posts/(hot|new|best|feed)/$', views.posts, name='posts'),

    url(r'^posts/([0-9]+)/$', views.comments, name='comments'),

    url(r'^blogs/$', RedirectView.as_view(url='/blogs/best/', permanent=True)),
    url(r'^blogs/(best|new|feed)/$', views.blogs, name='blogs'),

    url(r'^people/$', views.people, name='people'),
    url(r'^about/$', views.about, name='about'),

    url(r'^robots.txt$', TemplateView.as_view(template_name='blog/robots.txt', content_type='text/plain')),
    url(r'^humans.txt$', TemplateView.as_view(template_name='blog/humans.txt', content_type='text/plain')),

    # API (GET)

    url(r'^api/posts.get$', views.posts_get, name='api'),
    url(r'^api/blogs.get$', views.blogs_get, name='api'),
    url(r'^api/users.get$', views.users_get, name='api'),

    url(r'^api/posts.getById$', views.posts_getById, name='api'),
    url(r'^api/blogs.getById$', views.blogs_getById, name='api'),
    url(r'^api/users.getById$', views.users_getById, name='api'),

    url(r'^api/comments.get$', views.comments_get, name='api'),

    url(r'^api/posts.getFollowers$', views.posts_getFollowers, name='api'),
    url(r'^api/blogs.getFollowers$', views.blogs_getFollowers, name='api'),
    url(r'^api/users.getFollowers$', views.users_getFollowers, name='api'),

    url(r'^api/users.getSubscriptionsForPosts$', views.users_getSubscriptionsForPosts, name='api'),
    url(r'^api/users.getSubscriptionsForBlogs$', views.users_getSubscriptionsForBlogs, name='api'),

    # API (POST)

    url(r'^api/posts.subscribe$', views.posts_subscribe, name='api'),
    url(r'^api/blogs.subscribe$', views.blogs_subscribe, name='api'),
    url(r'^api/users.subscribe$', views.users_subscribe, name='api'),

    url(r'^api/posts.vote$', views.posts_vote, name='api'),
    url(r'^api/comments.vote$', views.comments_vote, name='api'),

    # 404 page

    url(r'^(?!admin$).*/$', views.page_404, name='page_404'),
]
