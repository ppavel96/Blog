from django.shortcuts import render

def posts(request, category = "hot"):
    return render(request, 'blog/posts.html', { 'navigation' : 'posts', 'category' : category })

def people(request):
    return render(request, 'blog/people.html', { 'navigation' : 'people' })

def blogs(request):
    return render(request, 'blog/blogs.html', { 'navigation' : 'blogs' })

def about(request):
    return render(request, 'blog/about.html', { 'navigation' : 'about' })

def page_404(request):
    return render(request, 'blog/404.html', { 'navigation' : '404' })
