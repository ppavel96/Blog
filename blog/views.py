from django.shortcuts import render

def main_page(request):
    return render(request, 'blog/main_page.html', {})
