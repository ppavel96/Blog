﻿from django.conf.urls import url
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

    url(r'^api/posts.get$', views.posts_get, name='api'), # posts.get(category, older, newwer, better, worse, id, count, return_only_ids) --> array of posts in JSON or their ids only
    url(r'^api/blogs.get$', views.blogs_get, name='api'), # blogs.get(category, older, newwer, better, worse, id, count, return_only_ids) --> array of blogs in JSON or their ids only
    url(r'^api/users.get$', views.users_get, name='api'), # users.get(category, older, newwer, better, worse, id, count, return_only_ids) --> array of users in JSON or their ids only

    url(r'^api/posts.getById$', views.posts_getById, name='api'), # posts.getById(id) --> post in JSON
    url(r'^api/blogs.getById$', views.blogs_getById, name='api'), # blogs.getById(id) --> blog in JSON
    url(r'^api/users.getById$', views.users_getById, name='api'), # users.getById(id) --> user in JSON

    url(r'^api/comments.get$', views.comments_get, name='api'),
    url(r'^api/comments.getByPost$', views.comments_get, name='api'),
    url(r'^api/comments.getByUser$', views.comments_get, name='api'),

    url(r'^api/posts.getFollowers$', views.posts_getFollowers, name='api'), # posts.getFollowers(post_id, older, newwer, better, worse, id, count, return_only_ids) --> array of users in JSON or their ids only
    url(r'^api/blogs.getFollowers$', views.blogs_getFollowers, name='api'), # blogs.getFollowers(blog_id, older, newwer, better, worse, id, count, return_only_ids) --> array of users in JSON or their ids only
    url(r'^api/users.getFollowers$', views.users_getFollowers, name='api'), # users.getFollowers(user_id, older, newwer, better, worse, id, count, return_only_ids) --> array of users in JSON or their ids only

    url(r'^api/users.getSubscriptionsForPosts$', views.users_getSubscriptionsForPosts, name='api'), # users.getSubscriptionsForPosts(user_id, older, newwer, better, worse, id, count, return_only_ids) --> array of posts in JSON or their ids only
    url(r'^api/users.getSubscriptionsForBlogs$', views.users_getSubscriptionsForBlogs, name='api'), # users.getSubscriptionsForBlogs(user_id, older, newwer, better, worse, id, count, return_only_ids) --> array of blogs in JSON or their ids only
    url(r'^api/users.getSubscriptionsForUsers$', views.users_getSubscriptionsForBlogs, name='api'), # users.getSubscriptionsForUsers(user_id, older, newwer, better, worse, id, count, return_only_ids) --> array of users in JSON or their ids only

    # isSubscribed
    # isFollower
    # getVote

    # API (POST)

    url(r'^api/users.subscribeForPost$', views.users_subscribeForPost, name='api'), # users.subscribeForPost(subscriber_id, post_id, subscribe)
    url(r'^api/users.subscribeForBlog$', views.users_subscribeForBlog, name='api'), # users.subscribeForBlog(subscriber_id, blog_id, subscribe)
    url(r'^api/users.subscribeForUser$', views.users_subscribeForUser, name='api'), # users.subscribeForUser(subscriber_id, user_id, subscribe)

    url(r'^api/users.voteForPost$', views.users_voteForPost, name='api'),           # users.voteForPost(user_id, post_id, vote)
    url(r'^api/users.voteForBlog$', views.users_voteForBlog, name='api'),           # users.voteForBlog(user_id, post_id, vote)
    url(r'^api/users.voteForComment$', views.users_voteForComment, name='api'),     # users.voteForComment(user_id, post_id, vote)

    # 404 page

    url(r'^(?!admin$).*/$', views.page_404, name='page_404'),
]
