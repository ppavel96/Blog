from django.shortcuts import render
from django.http import JsonResponse
from blog.models import *

def posts(request, category = "hot"):
    return render(request, 'blog/posts.html', { 'navigation' : 'posts', 'category' : category })

def people(request):
    return render(request, 'blog/people.html', { 'navigation' : 'people' })

def blogs(request, category = 'best'):
    return render(request, 'blog/blogs.html', { 'navigation' : 'blogs', 'category' : category })

def about(request):
    return render(request, 'blog/about.html', { 'navigation' : 'about' })

def ajax(request):
    id = int(request.GET.get('id', '0'))
    count = int(request.GET.get('count', '0'))

    response = []
    array = []

    if request.GET.get('navigation', '') == 'posts':
        if request.GET.get('category', '') == 'hot':
            array = Post.objects.order_by('publishedDate')
        elif request.GET.get('category', '') == 'new':
            array = Post.objects.order_by('-publishedDate')
        elif request.GET.get('category', '') == 'best':
            array = Post.objects.order_by('-rating')
        else:
            array = Post.objects.all()

    for i in array[id:id + count]:
        response.append(i.getDict())

    return JsonResponse(response, safe=False)

def page_404(request):
    response = render(request, 'blog/404.html', { 'navigation' : '404' })
    response.status_code = 404
    return response
