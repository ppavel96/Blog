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

# API (GET)

def posts_get(request):
    try:
        category = request.GET.get('category', '')

        older = request.GET.get('older', '')
        newer = request.GET.get('newer', '')

        better = request.GET.get('better', '')
        worse = request.GET.get('worse', '')

        id = int(request.GET.get('id', '0'))
        count = int(request.GET.get('count', '0'))

        array = []
        if category == 'hot' or category == 'new':
            array = Post.objects.all().order_by('publishedDate')
        if category == 'best':
            array = Post.objects.all().order_by('cachedRating')

        if older != '':
            array = array.filter(publishedDate__lt=older)
        if newer != '':
            array = array.filter(publishedDate__gt=newer)

        if better != '':
            array = array.filter(cachedRating__gt=better)
        if worse != '':
            array = array.filter(cachedRating__lt=worse)

        response = []

        for i in array[id:id + count]:
            response.append(i.getDict())

        return JsonResponse(response, safe=False)

    except:
        return JsonResponse([], safe=False)


def blogs_get(request):
    try:
        category = request.GET.get('category', '')

        older = request.GET.get('older', '')
        newer = request.GET.get('newer', '')

        id = int(request.GET.get('id', '0'))
        count = int(request.GET.get('count', '0'))

        array = []
        if category == 'new':
            array = Blog.objects.all().order_by('publishedDate')
        if category == 'best':
            array = Blog.objects.all().order_by('cachedBlogRating')

        if older != '':
            array = array.filter(publishedDate__lt=older)
        if newer != '':
            array = array.filter(publishedDate__gt=newer)

        response = []

        for i in array[id:id + count]:
            response.append(i.getDict())

        return JsonResponse(response, safe=False)

    except:
        return JsonResponse([], safe=False)


def users_get(request):
    try:
        older = request.GET.get('older', '')
        newer = request.GET.get('newer', '')

        better = request.GET.get('better', '')
        worse = request.GET.get('worse', '')

        id = int(request.GET.get('id', '0'))
        count = int(request.GET.get('count', '0'))

        array = Profile.objects.all()

        if older != '':
            array = array.filter(user__date_joined__lt=older)
        if newer != '':
            array = array.filter(user__date_joined__gt=newer)

        if better != '':
            array = array.filter(cachedRating__gt=better)
        if worse != '':
            array = array.filter(cachedRating__lt=worse)

        response = []

        for i in array[id:id + count]:
            response.append(i.getDict())

        return JsonResponse(response, safe=False)

    except:
        return JsonResponse([], safe=False)


def posts_getById(request):
    try:
        post = Post.objects.get(id=request.GET.get('id', ''))
        return JsonResponse([post.getDict()], safe=False)

    except:
        return JsonResponse([], safe=False)


def blogs_getById(request):
    try:
        blog = Blog.objects.get(id=request.GET.get('id', ''))
        return JsonResponse([blog.getDict()], safe=False)

    except:
        return JsonResponse([], safe=False)


def users_getById(request):
    try:
        user = Profile.objects.get(id=request.GET.get('id', ''))
        return JsonResponse([user.getDict()], safe=False)

    except:
        return JsonResponse([], safe=False)


def comments_get(request):
    pass


def posts_getFollowers(request):
    try:
        post = Post.objects.get(id=request.GET.get('post_id', ''))
        
        id = int(request.GET.get('id', '0'))
        count = int(request.GET.get('count', '0'))

        older = request.GET.get('older', '')
        newer = request.GET.get('newer', '')

        better = request.GET.get('better', '')
        worse = request.GET.get('worse', '')

        array = post.profile_set.all()

        if older != '':
            array = array.filter(user__date_joined__lt=older)
        if newer != '':
            array = array.filter(user__date_joined__gt=newer)

        if better != '':
            array = array.filter(cachedRating__gt=better)
        if worse != '':
            array = array.filter(cachedRating__lt=worse)

        response = []

        for i in array[id:id + count]:
            response.append(i.getDict())

        return JsonResponse(response, safe=False)

    except:
        return JsonResponse([], safe=False)


def blogs_getFollowers(request):
    try:
        blog = Blog.objects.get(id=request.GET.get('blog_id', ''))
        
        id = int(request.GET.get('id', '0'))
        count = int(request.GET.get('count', '0'))

        older = request.GET.get('older', '')
        newer = request.GET.get('newer', '')

        better = request.GET.get('better', '')
        worse = request.GET.get('worse', '')

        array = blog.profile_set.all()

        if older != '':
            array = array.filter(user__date_joined__lt=older)
        if newer != '':
            array = array.filter(user__date_joined__gt=newer)

        if better != '':
            array = array.filter(cachedRating__gt=better)
        if worse != '':
            array = array.filter(cachedRating__lt=worse)

        response = []

        for i in array[id:id + count]:
            response.append(i.getDict())

        return JsonResponse(response, safe=False)

    except:
        return JsonResponse([], safe=False)


def users_getFollowers(request):
    try:
        user = Profile.objects.get(id=request.GET.get('user_id', ''))
        
        id = int(request.GET.get('id', '0'))
        count = int(request.GET.get('count', '0'))

        older = request.GET.get('older', '')
        newer = request.GET.get('newer', '')

        better = request.GET.get('better', '')
        worse = request.GET.get('worse', '')

        array = user.profile_set.all()

        if older != '':
            array = array.filter(user__date_joined__lt=older)
        if newer != '':
            array = array.filter(user__date_joined__gt=newer)

        if better != '':
            array = array.filter(cachedRating__gt=better)
        if worse != '':
            array = array.filter(cachedRating__lt=worse)

        response = []

        for i in array[id:id + count]:
            response.append(i.getDict())

        return JsonResponse(response, safe=False)

    except:
        return JsonResponse([], safe=False)


def users_getSubscriptionsForPosts(request):
    pass


def users_getSubscriptionsForBlogs(request):
    pass


# API (POST)

def posts_subscribe(request):
    pass


def blogs_subscribe(request):
    pass


def users_subscribe(request):
    pass


def posts_vote(request):
    pass


def comments_vote(request):
    pass


# 404 page

def page_404(request):
    response = render(request, 'blog/404.html', { 'navigation' : '404' })
    response.status_code = 404
    return response
