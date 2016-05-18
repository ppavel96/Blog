from django.shortcuts import render
from django.http import JsonResponse
from blog.models import *


# Pages

def posts(request, category = 'hot'):
    return render(request, 'blog/posts.html', { 'navigation' : 'posts', 'category' : category })

def people(request):
    return render(request, 'blog/people.html', { 'navigation' : 'people' })

def blogs(request, category = 'best'):
    return render(request, 'blog/blogs.html', { 'navigation' : 'blogs', 'category' : category })

def about(request):
    return render(request, 'blog/about.html', { 'navigation' : 'about' })

def comments(request, id = '0'):
    if Post.objects.filter(id=id).count() > 0:
        return render(request, 'blog/comments.html', { 'navigation' : 'posts', 'id' : id })
    
    return page_404(request)


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

        array = []
        if category == 'new':
            array = Post.objects.all().order_by('publishedDate')
        if category == 'best':
            array = Post.objects.all().order_by('cachedRating')

        return JsonResponse(to_JSON(request, filter_posts(request, array)), safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


def blogs_get(request):
    try:
        category = request.GET.get('category', '')

        array = []
        if category == 'new':
            array = Blog.objects.all().order_by('publishedDate')
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
    pass


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
    response = render(request, 'blog/404.html', { 'navigation' : '404' })
    response.status_code = 404
    return response
