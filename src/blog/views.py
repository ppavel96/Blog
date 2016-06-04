from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout

from blog.models import *


# Pages

def posts(request, category = 'new'):
    if not request.user.is_authenticated() and category == 'feed':
        return redirect('/posts/new/')

    return render(request, 'blog/posts.html', { 'navigation' : 'posts', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'category' : category })

def people(request):
    return render(request, 'blog/people.html', { 'navigation' : 'people', 'tags' : Tag.objects.all().order_by('cachedTagNumber') })

def blogs(request, category = 'best'):
    if not request.user.is_authenticated() and category == 'feed':
        return redirect('/blogs/new/')

    return render(request, 'blog/blogs.html', { 'navigation' : 'blogs', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'category' : category })

def about(request):
    return render(request, 'blog/about.html', { 'navigation' : 'about', 'tags' : Tag.objects.all().order_by('cachedTagNumber') })

def comments(request, id = '0'):
    if Post.objects.filter(id=id).count() > 0:
        return render(request, 'blog/comments.html', { 'navigation' : 'posts', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'post' : Post.objects.get(id=id) })
    
    return page_404(request)

def search(request, tag = ''):
    return render(request, 'blog/search.html', { 'navigation' : 'posts', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'category' : 'tag_' + tag })

def blog_search(request, blog = '0'):
    if Blog.objects.filter(id=blog).count() > 0:
        return render(request, 'blog/blog_search.html', { 'navigation' : 'posts', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'category' : 'blog_' + blog, 'blog_name' : Blog.objects.get(id=blog).title })

    return page_404(request)

def login_view(request):
    if request.method == 'POST':
        try:
            username= request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return JsonResponse({ 'result' : 'ok' }, safe=False)
            else:
                return JsonResponse({ 'result' : 'incorrect' }, safe=False)

        except:
            return JsonResponse(['Error'], safe=False)

    return page_404(request)

def logout_view(request):
    if request.method == 'POST':
        try:
            logout(request)
            return JsonResponse({ 'result' : 'ok' }, safe=False)

        except:
            return JsonResponse(['Error'], safe=False)

    return page_404(request)

def register(request):
    pass

def profile(request):
    pass


# API (Helper functions)

def parse_request(request):
    older = request.GET.get('older', '')
    newer = request.GET.get('newer', '')

    better = request.GET.get('better', '')
    worse = request.GET.get('worse', '')

    id = int(request.GET.get('id', '0'))
    count = int(request.GET.get('count', '0'))

    return older, newer, better, worse, id, count


def filter_posts(request, array):
    older, newer, better, worse, id, count = parse_request(request)

    if older != '':
        array = array.filter(publishedDate__lt=older)
    if newer != '':
        array = array.filter(publishedDate__gt=newer)

    if better != '':
        array = array.filter(cachedRating__gt=better)
    if worse != '':
        array = array.filter(cachedRating__lt=worse)

    return array[id:id + count]


def filter_blogs(request, array):
    older, newer, better, worse, id, count = parse_request(request)

    if older != '':
        array = array.filter(publishedDate__lt=older)
    if newer != '':
        array = array.filter(publishedDate__gt=newer)

    if better != '':
        array = array.filter(cachedBlogRating__gt=better)
    if worse != '':
        array = array.filter(cachedBlogRating__lt=worse)

    return array[id:id + count]


def filter_users(request, array):
    older, newer, better, worse, id, count = parse_request(request)

    if older != '':
        array = array.filter(user__date_joined__lt=older)
    if newer != '':
        array = array.filter(user__date_joined__gt=newer)

    if better != '':
        array = array.filter(cachedUserRating__gt=better)
    if worse != '':
        array = array.filter(cachedUserRating__lt=worse)

    return array[id:id + count]


def filter_comments(request, array):
    older, newer, better, worse, id, count = parse_request(request)

    if older != '':
        array = array.filter(publishedDate__lt=older)
    if newer != '':
        array = array.filter(publishedDate__gt=newer)

    if better != '':
        array = array.filter(cachedRating__gt=better)
    if worse != '':
        array = array.filter(cachedRating__lt=worse)

    return array[id:id + count]


def to_JSON(request, array):
    return_only_ids =  int(request.GET.get('return_only_ids', '0'))
    if return_only_ids == 1:
        return [i.id for i in array]
    else:
        return [i.to_JSON() for i in array]


# API (GET)

def posts_get(request):
    try:
        category = request.GET.get('category', '')

        if category == 'new':
            array = Post.objects.all().order_by('-publishedDate')
        if category == 'best':
            array = Post.objects.all().order_by('cachedRating')

        if category[:4] == 'tag_':
            actual_tag = Tag.objects.all().get(name=category[4:])
            array = Post.objects.all().filter(tags__in=[actual_tag]).order_by('-publishedDate')

        if category[:5] == 'blog_':
            actual_blog = Blog.objects.all().get(id=category[5:])
            array = Post.objects.all().filter(blog__in=[actual_blog]).order_by('-publishedDate')

        return JsonResponse(to_JSON(request, filter_posts(request, array)), safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


def blogs_get(request):
    try:
        category = request.GET.get('category', '')

        if category == 'new':
            array = Blog.objects.all().order_by('-publishedDate')
        if category == 'best':
            array = Blog.objects.all().order_by('cachedBlogRating')

        return JsonResponse(to_JSON(request, filter_blogs(request, array)), safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


def users_get(request):
    try:
        return JsonResponse(to_JSON(request, filter_users(request, Profile.objects.all().order_by('cachedUserRating'))), safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


def posts_getById(request):
    try:
        post = Post.objects.get(id=request.GET.get('id', ''))
        return JsonResponse([post.to_JSON()], safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


def blogs_getById(request):
    try:
        blog = Blog.objects.get(id=request.GET.get('id', ''))
        return JsonResponse([blog.to_JSON()], safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


def users_getById(request):
    try:
        user = Profile.objects.get(id=request.GET.get('id', ''))
        return JsonResponse([user.to_JSON()], safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


def comments_get(request):
    try:
        return JsonResponse(to_JSON(request, filter_comments(request, Comment.objects.all().order_by('cachedRating'))), safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


def comments_getByPost(request):
    pass


def comments_getByUser(request):
    try:
        user = Profile.objects.get(id=request.GET.get('user_id', ''))
        array = user.comment_set.all()

        return JsonResponse(to_JSON(request, filter_comments(request, array)), safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


def posts_getFollowers(request):
    try:
        post = Post.objects.get(id=request.GET.get('post_id', ''))
        array = post.profile_set.all()

        return JsonResponse(to_JSON(request, filter_users(request, array)), safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


def blogs_getFollowers(request):
    try:
        blog = Blog.objects.get(id=request.GET.get('blog_id', ''))
        array = blog.profile_set.all()

        return JsonResponse(to_JSON(request, filter_users(request, array)), safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


def users_getFollowers(request):
    try:
        user = Profile.objects.get(id=request.GET.get('user_id', ''))
        array = user.profile_set.all()

        return JsonResponse(to_JSON(request, filter_users(request, array)), safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


def users_getSubscriptionsForPosts(request):
    try:
        user = Profile.objects.get(id=request.GET.get('user_id', ''))
        array = user.followedPosts.all()

        return JsonResponse(to_JSON(request, filter_posts(request, array)), safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


def users_getSubscriptionsForBlogs(request):
    try:
        user = Profile.objects.get(id=request.GET.get('user_id', ''))
        array = user.followedBlogs.all()

        return JsonResponse(to_JSON(request, filter_blogs(request, array)), safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


def users_getSubscriptionsForUsers(request):
    try:
        user = Profile.objects.get(id=request.GET.get('user_id', ''))
        array = user.followedUsers.all()

        return JsonResponse(to_JSON(request, filter_users(request, array)), safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


# API (POST)

def users_subscribeForPost(request):
    pass


def users_subscribeForBlog(request):
    pass


def users_subscribeForUser(request):
    pass


def users_voteForPost(request):
    pass


def users_voteForBlog(request):
    pass


def users_voteForComment(request):
    pass


# 404 page

def page_404(request):
    response = render(request, 'blog/404.html', { 'navigation' : '404', 'tags' : Tag.objects.all().order_by('cachedTagNumber') })
    response.status_code = 404
    return response
