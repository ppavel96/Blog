from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q

from PIL import Image
import re, datetime

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
        return render(request, 'blog/comments.html', { 'navigation' : 'posts', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'post' : Post.objects.get(id=id), 'post_json' : Post.objects.get(id=id).to_JSON(request.user) })
    
    return page_404(request)

def search(request, tag = ''):
    return render(request, 'blog/search.html', { 'navigation' : 'posts', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'category' : 'tag_' + tag })

def publications(request, user = '0'):
    if Profile.objects.filter(id=user).count() > 0:
        return render(request, 'blog/publications.html', { 'navigation' : 'posts', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'category' : 'user_' + user, 'user_name' : Profile.objects.get(id=user).user.username })

def blog_search(request, blog = '0'):
    if Blog.objects.filter(id=blog).count() > 0:
        return render(request, 'blog/blog_search.html', { 'navigation' : 'posts', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'category' : 'blog_' + blog, 'blog_name' : Blog.objects.get(id=blog).title })

    return page_404(request)

def login_view(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
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
    if request.method == 'GET':
        if request.user.is_authenticated():
            return redirect('/posts/new/')

        return render(request, 'blog/register.html', { 'navigation' : 'register', 'tags' : Tag.objects.all().order_by('cachedTagNumber') })
    else:
        try:
            username = request.POST.get('username').strip()
            email = request.POST.get('email').strip()

            password = request.POST.get('password')
            password_repeat = request.POST.get('password_repeat')

            firstname = request.POST.get('firstname').strip()
            lastname = request.POST.get('lastname').strip()

            birth = request.POST.get('birth').strip()
            gender = request.POST.get('gender').strip()
            country = request.POST.get('country').strip()
            city = request.POST.get('city').strip()

            facebook = request.POST.get('facebook').strip()
            twitter = request.POST.get('twitter').strip()
            vk = request.POST.get('vk').strip()

            if len(username) < 2 or len(username) > 20:
                return JsonResponse({ 'result' : 'usernameError',  'message' : 'Username\'s length should be between 2 and 20' }, safe=False)

            if not re.match('[0-9|A-Z|a-z|_]+$', username):
                return JsonResponse({ 'result' : 'usernameError',  'message' : 'Username contains invalid characters' }, safe=False)

            if User.objects.filter(username=username).count() > 0:
                return JsonResponse({ 'result' : 'usernameError',  'message' : 'Username is already in use' }, safe=False)

            if 'avatar' in request.FILES:
                try:
                    Image.open(request.FILES['avatar']).verify()
                except:
                    return JsonResponse({ 'result' : 'usernameError',  'message' : 'Avatar file does not look like an image' }, safe=False)

                if request.FILES['avatar']._size > 1024 * 512:
                    return JsonResponse({ 'result' : 'usernameError',  'message' : 'Avatar size exceeds limit (' + str(request.FILES['avatar']._size // 1024) + ' KB > 500 KB)' }, safe=False)

            if not re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({ 'result' : 'emailError',     'message' : 'Email is invalid' }, safe=False)

            if len(firstname) < 2 or len(firstname) > 20:
                return JsonResponse({ 'result' : 'firstnameError', 'message' : 'Firstname\'s length should be between 2 and 20' }, safe=False)

            if not re.match('[A-Z|a-z| ]+$', firstname):
                return JsonResponse({ 'result' : 'firstnameError', 'message' : 'Firstname contains invalid characters' }, safe=False)

            if len(lastname) < 2 or len(lastname) > 20:
                return JsonResponse({ 'result' : 'lastnameError',  'message' : 'Lastname\'s length should be between 2 and 20' }, safe=False)

            if not re.match('[A-Z|a-z| ]+$', lastname):
                return JsonResponse({ 'result' : 'lastnameError', 'message' : 'Lastname contains invalid characters' }, safe=False)

            if len(password) < 6:
                return JsonResponse({ 'result' : 'passwordError',  'message' : 'Password should be at least 6 characters long' }, safe=False)

            if password != password_repeat:
                return JsonResponse({ 'result' : 'password_repeatError', 'message' : 'Passwords do not match' }, safe=False)

            if len(birth) > 0:
                if not re.match('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$', birth):
                    return JsonResponse({ 'result' : 'birthError', 'message' : 'Date is in incorrect format' }, safe=False)

                try:
                    temp = datetime.date(year=int(birth[0:4]), month=int(birth[5:7]), day=int(birth[8:10]))
                except:
                    return JsonResponse({ 'result' : 'birthError', 'message' : 'Date is invalid' }, safe=False)
                
            if len(gender) > 0 and not gender in ("Male", "Female"):
                return JsonResponse({ 'result' : 'genderError', 'message' : '"Male" or "Female" only!' }, safe=False)

            if len(country) > 0 and not re.match('[A-Z|a-z| ]+$', country):
                return JsonResponse({ 'result' : 'countryError',  'message' : 'Country contains invalid characters' }, safe=False)

            if len(city) > 0 and not re.match('[A-Z|a-z| ]+$', city):
                return JsonResponse({ 'result' : 'cityError',  'message' : 'City contains invalid characters' }, safe=False)

            profile = Profile(dateOfBirth=birth, gender=gender, country=country, city=city, facebook=facebook, twitter=twitter, vk=vk)
            if 'avatar' in request.FILES:
                profile.image = request.FILES['avatar']

            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname

            user.save()

            profile.user = user;
            profile.save()

            user = authenticate(username=username, password=password)
            login(request, user)

            return JsonResponse({ 'result' : 'ok' }, safe=False)

        except:
            return JsonResponse(['Error'], safe=False)

def profile(request, profile = '0'):
    if Profile.objects.filter(id=profile).count() > 0:
        if request.user.is_authenticated() and request.user.profile.id == int(profile):
            return render(request, 'blog/profile.html', { 'navigation' : 'profile', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'profile' : Profile.objects.get(id=profile), 'is_subscribed' : Profile.objects.get(id=profile).is_followed_by(request.user) })
        else:
            return render(request, 'blog/profile.html', { 'navigation' : 'people', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'profile' : Profile.objects.get(id=profile), 'is_subscribed' : Profile.objects.get(id=profile).is_followed_by(request.user) })

    return page_404(request)

def profile_favorites(request, profile = '0'):
    if Profile.objects.filter(id=profile).count() > 0:
        if request.user.is_authenticated() and request.user.profile.id == int(profile):
            return render(request, 'blog/profile_favorites.html', { 'navigation' : 'profile', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'profile' : Profile.objects.get(id=profile) })
        else:
            return render(request, 'blog/profile_favorites.html', { 'navigation' : 'people', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'profile' : Profile.objects.get(id=profile) })

    return page_404(request)

def profile_followers(request, profile = '0'):
    if Profile.objects.filter(id=profile).count() > 0:
        if request.user.is_authenticated() and request.user.profile.id == int(profile):
            return render(request, 'blog/profile_followers.html', { 'navigation' : 'profile', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'profile' : Profile.objects.get(id=profile) })
        else:
            return render(request, 'blog/profile_followers.html', { 'navigation' : 'people', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'profile' : Profile.objects.get(id=profile) })

    return page_404(request)

def profile_subscriptions(request, profile = '0'):
    if Profile.objects.filter(id=profile).count() > 0:
        if request.user.is_authenticated() and request.user.profile.id == int(profile):
            return render(request, 'blog/profile_subscriptions.html', { 'navigation' : 'profile', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'profile' : Profile.objects.get(id=profile) })
        else:
            return render(request, 'blog/profile_subscriptions.html', { 'navigation' : 'people', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'profile' : Profile.objects.get(id=profile) })

    return page_404(request)

def profile_edit(request, profile = '0'):
    if request.method == 'GET':
        if Profile.objects.filter(id=profile).count() > 0:
            if request.user.is_authenticated() and request.user.profile.id == int(profile):
                return render(request, 'blog/profile_edit.html', { 'navigation' : 'profile', 'tags' : Tag.objects.all().order_by('cachedTagNumber'), 'profile' : Profile.objects.get(id=profile) })
            else:
                return redirect('/profile/' + profile + '/')

        return page_404(request)
    else:
        try:
            if request.user.is_authenticated() and request.user.profile.id == int(profile):
                email = request.POST.get('email').strip()

                firstname = request.POST.get('firstname').strip()
                lastname = request.POST.get('lastname').strip()

                birth = request.POST.get('birth').strip()
                gender = request.POST.get('gender').strip()
                country = request.POST.get('country').strip()
                city = request.POST.get('city').strip()

                facebook = request.POST.get('facebook').strip()
                twitter = request.POST.get('twitter').strip()
                vk = request.POST.get('vk').strip()

                newpassword = request.POST.get('newpassword')
                newpassword_repeat = request.POST.get('newpassword_repeat')

                password = request.POST.get('password')

                if 'avatar' in request.FILES:
                    try:
                        Image.open(request.FILES['avatar']).verify()
                    except:
                        return JsonResponse({ 'result' : 'emailError',  'message' : 'Avatar file does not look like an image' }, safe=False)

                    if request.FILES['avatar']._size > 1024 * 512:
                        return JsonResponse({ 'result' : 'emailError',  'message' : 'Avatar size exceeds limit (' + str(request.FILES['avatar']._size // 1024) + ' KB > 500 KB)' }, safe=False)

                if not re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                    return JsonResponse({ 'result' : 'emailError',     'message' : 'Email is invalid' }, safe=False)

                if len(firstname) < 2 or len(firstname) > 20:
                    return JsonResponse({ 'result' : 'firstnameError', 'message' : 'Firstname\'s length should be between 2 and 20' }, safe=False)

                if not re.match('[A-Z|a-z| ]+$', firstname):
                    return JsonResponse({ 'result' : 'firstnameError', 'message' : 'Firstname contains invalid characters' }, safe=False)

                if len(lastname) < 2 or len(lastname) > 20:
                    return JsonResponse({ 'result' : 'lastnameError',  'message' : 'Lastname\'s length should be between 2 and 20' }, safe=False)

                if not re.match('[A-Z|a-z| ]+$', lastname):
                    return JsonResponse({ 'result' : 'lastnameError', 'message' : 'Lastname contains invalid characters' }, safe=False)

                if len(birth) > 0:
                    if not re.match('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$', birth):
                        return JsonResponse({ 'result' : 'birthError', 'message' : 'Date is in incorrect format' }, safe=False)

                    try:
                        temp = datetime.date(year=int(birth[0:4]), month=int(birth[5:7]), day=int(birth[8:10]))
                    except:
                        return JsonResponse({ 'result' : 'birthError', 'message' : 'Date is invalid' }, safe=False)
                
                if len(gender) > 0 and not gender in ("Male", "Female"):
                    return JsonResponse({ 'result' : 'genderError', 'message' : '"Male" or "Female" only!' }, safe=False)

                if len(country) > 0 and not re.match('[A-Z|a-z| ]+$', country):
                    return JsonResponse({ 'result' : 'countryError',  'message' : 'Country contains invalid characters' }, safe=False)

                if len(city) > 0 and not re.match('[A-Z|a-z| ]+$', city):
                    return JsonResponse({ 'result' : 'cityError',  'message' : 'City contains invalid characters' }, safe=False)

                if len(newpassword) > 0:
                    if len(newpassword) < 6:
                        return JsonResponse({ 'result' : 'newpasswordError',  'message' : 'Password should be at least 6 characters long' }, safe=False)

                    if newpassword != newpassword_repeat:
                        return JsonResponse({ 'result' : 'newpassword_repeatError', 'message' : 'Passwords do not match' }, safe=False)

                if not request.user.check_password(password):
                    return JsonResponse({ 'result' : 'passwordError', 'message' : 'Incorrect password' }, safe=False)

                request.user.email = email
                request.user.first_name = firstname
                request.user.last_name = lastname

                if len(newpassword) > 0:
                    request.user.set_password(newpassword)
                    logout(request)

                request.user.save()

                request.user.profile.dateOfBirth = birth
                request.user.profile.gender=gender
                request.user.profile.country=country
                request.user.profile.city=city
                request.user.profile.facebook=facebook
                request.user.profile.twitter=twitter
                request.user.profile.vk = vk

                if 'avatar' in request.FILES:
                    request.user.profile.image = request.FILES['avatar']

                request.user.profile.save()

                return JsonResponse({ 'result' : 'ok' }, safe=False)
            else:
                return JsonResponse(['Error'], safe=False)
        except:
            return JsonResponse(['Error'], safe=False)


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
        return [i.to_JSON(request.user) for i in array]


# API (GET)

def posts_get(request):
    try:
        category = request.GET.get('category', '')

        if category == 'new':
            array = Post.objects.all().order_by('-publishedDate')
        if category == 'best':
            array = Post.objects.all().order_by('-cachedRating')
        if category == 'feed':
            if not request.user.is_authenticated():
                array = Post.objects.filter(id=-1)
            else:
                array = Post.objects.filter(Q(author__profile__in=request.user.profile.followedUsers.all()) | Q(blog__in=request.user.profile.followedBlogs.all())).order_by('-publishedDate')

        if category[:4] == 'tag_':
            actual_tag = Tag.objects.all().get(name=category[4:])
            array = Post.objects.all().filter(tags__in=[actual_tag]).order_by('-publishedDate')

        if category[:5] == 'blog_':
            actual_blog = Blog.objects.all().get(id=category[5:])
            array = Post.objects.all().filter(blog__in=[actual_blog]).order_by('-publishedDate')

        if category[:5] == 'user_':
            actual_user = Profile.objects.all().get(id=category[5:]).user
            array = Post.objects.all().filter(author__in=[actual_user]).order_by('-publishedDate')

        return JsonResponse(to_JSON(request, filter_posts(request, array)), safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


def blogs_get(request):
    try:
        category = request.GET.get('category', '')

        if category == 'new':
            array = Blog.objects.all().order_by('-publishedDate')
        if category == 'best':
            array = Blog.objects.all().order_by('-cachedBlogRating')
        if category == 'feed':
            array = request.user.profile.followedBlogs.all().order_by('-cachedBlogRating')

        return JsonResponse(to_JSON(request, filter_blogs(request, array)), safe=False)

    except:
        return JsonResponse(['Error'], safe=False)


def users_get(request):
    try:
        return JsonResponse(to_JSON(request, filter_users(request, Profile.objects.all().order_by('-cachedUserRating'))), safe=False)

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
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=request.POST.get('post_id', ''))
            subscriber = Profile.objects.get(id=request.POST.get('subscriber_id', ''))
            subscribe = request.POST.get('subscribe', '0')

            if subscriber.followedPosts.filter(id=post.id).count() == 0 and subscribe == '1':
                subscriber.cachedSubscriptionsForPostNumber += 1
                post.cachedPostFollowersNumber += 1

                subscriber.followedPosts.add(post)

                subscriber.save()
                post.save()

            if subscriber.followedPosts.filter(id=post.id).count() > 0 and subscribe == '0':
                subscriber.cachedSubscriptionsForPostNumber -= 1
                post.cachedPostFollowersNumber -= 1

                subscriber.followedPosts.remove(post)

                subscriber.save()
                post.save()

            return JsonResponse({'result': 'ok'})

        except:
            return JsonResponse(['Error'], safe=False)

    return page_404(request)


def users_subscribeForBlog(request):
    if request.method == 'POST':
        try:
            blog = Blog.objects.get(id=request.POST.get('blog_id', ''))
            subscriber = Profile.objects.get(id=request.POST.get('subscriber_id', ''))
            subscribe = request.POST.get('subscribe', '0')

            if subscriber.followedBlogs.filter(id=blog.id).count() == 0 and subscribe == '1':
                subscriber.cachedSubscriptionsForBlogNumber += 1
                blog.cachedMembersNumber += 1

                subscriber.followedBlogs.add(blog)

                subscriber.save()
                blog.save()

            if subscriber.followedBlogs.filter(id=blog.id).count() > 0 and subscribe == '0':
                subscriber.cachedSubscriptionsForBlogNumber -= 1
                blog.cachedMembersNumber -= 1

                subscriber.followedBlogs.remove(blog)

                subscriber.save()
                blog.save()

            return JsonResponse({'result': 'ok'})

        except:
            return JsonResponse(['Error'], safe=False)

    return page_404(request)


def users_subscribeForUser(request):
    if request.method == 'POST':
        try:
            user = Profile.objects.get(id=request.POST.get('user_id', ''))
            subscriber = Profile.objects.get(id=request.POST.get('subscriber_id', ''))
            subscribe = request.POST.get('subscribe', '0')

            if subscriber.followedUsers.filter(id=user.id).count() == 0 and subscribe == '1':
                subscriber.cachedSubscriptionsForUserNumber += 1
                user.cachedFollowersNumber += 1

                subscriber.followedUsers.add(user)

                subscriber.save()
                user.save()

            if subscriber.followedUsers.filter(id=user.id).count() > 0 and subscribe == '0':
                subscriber.cachedSubscriptionsForUserNumber -= 1
                user.cachedFollowersNumber -= 1

                subscriber.followedUsers.remove(user)

                subscriber.save()
                user.save()

            return JsonResponse({'result': 'ok'})

        except:
            return JsonResponse(['Error'], safe=False)

    return page_404(request)


def users_voteForPost(request):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=request.POST.get('post_id', ''))
            user = Profile.objects.get(id=request.POST.get('user_id', ''))
            like = int(request.POST.get('vote', '0'))

            like = max(-1, min(1, like))

            if VoteForPost.objects.filter(user__profile=user, post=post).count() > 0:
                vote = VoteForPost.objects.get(user__profile=user, post=post)
                prev_like = vote.like
                vote.like = like
            else:
                prev_like = 0
                vote = VoteForPost(user=user.user, post=post, like=like)

            post.cachedRating += like - prev_like
            post.blog.cachedBlogRating += like - prev_like
            post.author.profile.cachedUserRating += like - prev_like

            post.save()
            post.blog.save()
            post.author.profile.save()
            vote.save()

            return JsonResponse({'result': 'ok'})

        except:
            return JsonResponse(['Error'], safe=False)

    return page_404(request)


def users_voteForComment(request):
    pass


# 404 page

def page_404(request):
    response = render(request, 'blog/404.html', { 'navigation' : '404', 'tags' : Tag.objects.all().order_by('cachedTagNumber') })
    response.status_code = 404
    return response
