from django.shortcuts import render

def posts(request):
    return render(request, 'blog/posts.html', {})

def people(request):
    return render(request, 'blog/people.html', {})

def blogs(request):
    return render(request, 'blog/blogs.html', {})

def about(request):
    return render(request, 'blog/about.html', {})
