from django.shortcuts import render
from django.http import JsonResponse
from blog.models import *

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
    else:
        return page_404(request)

def api(request):
    method = request.GET.get('method', '')

    if method in ('posts.get', 'blogs.get'):
        if method == 'posts.get':
            array = Post.objects.all()
        if method == 'blogs.get':
            array = Blog.objects.all()

        category = request.GET.get('category', '')
        older = request.GET.get('older', '')
        newer = request.GET.get('newer', '')

        if category == 'hot' and method == 'posts.get':
            array = array.order_by('publishedDate')
        if category == 'best' and method == 'posts.get':
            array = array.order_by('-rating')
        if category == 'new':
            array = array.order_by('-publishedDate')

        if older != '':
            array = array.filter(publishedDate__lt=older)

        if newer != '':
            array = array.filter(publishedDate__gt=newer)

        response = []

        id = int(request.GET.get('id', '0'))
        count = int(request.GET.get('count', '0'))

        for i in array[id:id + count]:
            response.append(i.getDict())

        return JsonResponse(response, safe=False)

    elif method == 'posts.getByID':
        try:
            post = Post.objects.get(id=request.GET.get('id', ''))
            return JsonResponse([post.getDict()], safe=False)

        except:
            return JsonResponse([], safe=False)

    return JsonResponse([], safe=False)

def page_404(request):
    response = render(request, 'blog/404.html', { 'navigation' : '404' })
    response.status_code = 404
    return response
