from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce, Value
from blog.storage import OverwriteStorage


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    blog = models.ForeignKey('Blog')

    title = models.CharField(max_length=200)
    content = models.TextField()

    publishedDate = models.DateTimeField(blank=True, null=True)

    tags = models.ManyToManyField('Tag', blank=True)

    # Cached

    cachedRating = models.IntegerField(default=0, editable=False)
    cachedCommentsNumber = models.PositiveIntegerField(default=0, editable=False)
    cachedPostFollowersNumber = models.PositiveIntegerField(default=0, editable=False)

    def recache(self):
        self.cachedRating = VoteForPost.objects.all().filter(post=self).aggregate(rating=Coalesce(Sum('like'), Value(0)))['rating']
        self.cachedCommentsNumber = Comment.objects.all().filter(post=self).count()
        self.cachedPostFollowersNumber = Profile.objects.all().filter(followedPosts__in=[self]).count()
        self.save()

    # JSON

    def is_followed_by(self, user):
        result = 0

        if user.is_authenticated() and Profile.objects.filter(user=user).count() > 0:
            profile = Profile.objects.get(user=user)
            if profile.followedPosts.filter(id=self.id).count() > 0:
                result = 1

        return result


    def get_vote(self, user):
        result = 0

        if user.is_authenticated() and VoteForPost.objects.filter(user=user, post__id=self.id).count() > 0:
            vote = VoteForPost.objects.get(user=user, post__id=self.id)
            result = vote.like

        return result


    def to_JSON(self, user):
        tags = list()
        for i in self.tags.all():
            tags.append(i.name)

        return { "author" : self.author.username,
                 "blog" : self.blog.__str__(),

                 "is_subscribed" : self.is_followed_by(user),
                 "vote" : self.get_vote(user),

                 "title" : self.title,
                 "content" : self.content,

                 "publishedDate" : self.publishedDate.isoformat(),

                 "tags" : tags,

                 "cachedRating" : self.cachedRating,
                 "cachedCommentsNumber" : self.cachedCommentsNumber,
                 "cachedPostFollowersNumber" : self.cachedPostFollowersNumber,

                 "id" : self.id,
                
                 "author_id" : self.author.profile.id,
                 "blog_id" : self.blog.id }


    def __str__(self):
        return self.title


class VoteForPost(models.Model):
    user = models.ForeignKey('auth.User')
    post = models.ForeignKey('Post')
    like = models.SmallIntegerField(default=0)

    def recache(self):
        pass

    def __str__(self):
        return self.user.__str__() + ' - ' + self.post.__str__()


class Tag(models.Model):
    name = models.CharField(max_length=10)

    # Cached

    cachedTagNumber = models.PositiveIntegerField(default=0, editable=False)

    def recache(self):
        self.cachedTagNumber = Post.objects.all().filter(tags__in=[self]).count()
        self.save()

    def __str__(self):
        return self.name + ' (' + self.cachedTagNumber.__str__() + ')'


class Comment(models.Model):
    author = models.ForeignKey('auth.User')
    post = models.ForeignKey('Post')

    content = models.TextField()

    publishedDate = models.DateTimeField(blank=True, null=True)
    
    # Cached

    cachedRating = models.IntegerField(default=0, editable=False)

    def recache(self):
        self.cachedRating = VoteForComment.objects.all().filter(comment=self).aggregate(rating=Coalesce(Sum('like'), Value(0)))['rating']
        self.save()

    # JSON

    def get_vote(self, user):
        result = 0

        if user.is_authenticated() and VoteForComment.objects.filter(user=user, comment__id=self.id).count() > 0:
            vote = VoteForComment.objects.get(user=user, comment__id=self.id)
            result = vote.like

        return result

    def to_JSON(self, user):
        return { 'author' : self.author.username,
                 'post' : self.post.title,

                 'image' : self.author.profile.image.url if self.author.profile.image else "",

                 "vote" : self.get_vote(user),

                 'author_id' : self.author.profile.id,
                 'post_id' : self.post.id,

                 'content' : self.content,

                 'publishedDate' : self.publishedDate.isoformat(),

                 'cachedRating' : self.cachedRating,

                 'id' : self.id }

    def __str__(self):
        return self.author.username + ' in "' + self.post.title + '"';


class VoteForComment(models.Model):
    user = models.ForeignKey('auth.User')
    comment = models.ForeignKey('Comment')
    like = models.SmallIntegerField(default=0)

    def recache(self):
        pass


def blog_avatar_path(instance, filename):
    return 'blog_avatars/{0}'.format(instance.id)


class Blog(models.Model):
    creator = models.ForeignKey('auth.User')

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=blog_avatar_path, storage=OverwriteStorage(), blank=True)

    description = models.TextField()

    publishedDate = models.DateTimeField(blank=True, null=True)

    # Cached

    cachedBlogRating = models.IntegerField(default=0, editable=False)
    cachedMembersNumber = models.PositiveIntegerField(default=0, editable=False)
    cachedPostsNumber = models.PositiveIntegerField(default=0, editable=False)

    def recache(self):
        self.cachedBlogRating = Post.objects.all().filter(blog=self).aggregate(blogRating=Coalesce(Sum('cachedRating'), Value(0)))['blogRating']
        self.cachedMembersNumber = Profile.objects.all().filter(followedBlogs__in=[self]).count()
        self.cachedPostsNumber = Post.objects.all().filter(blog=self).count()
        self.save()

    # JSON

    def is_followed_by(self, user):
        result = '0'

        if user.is_authenticated() and Profile.objects.filter(user=user).count() > 0:
            profile = Profile.objects.get(user=user)
            if profile.followedBlogs.filter(id=self.id).count() > 0:
                result = '1'

        return result


    def to_JSON(self, user):
        return { 'creator' : self.creator.username,
                 'creator_id' : self.creator.profile.id,

                 'is_subscribed' : self.is_followed_by(user),

                 'title' : self.title,
                 'image' : self.image.url if self.image else "",

                 'description' : self.description,

                 'publishedDate' : self.publishedDate.isoformat(),

                 'cachedBlogRating' : self.cachedBlogRating,
                 'cachedMembersNumber' : self.cachedMembersNumber,
                 'cachedPostsNumber' : self.cachedPostsNumber,

                 'id' : self.id }

    def __str__(self):
        return self.title


def user_avatar_path(instance, filename):
    return 'avatars/{0}'.format(instance.user.id)


class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_avatar_path, storage=OverwriteStorage(), blank=True)

    dateOfBirth = models.CharField(max_length=10, default="", blank=True)
    gender = models.CharField(max_length=6, default="", blank=True)
    country = models.CharField(max_length=20, default="", blank=True)
    city = models.CharField(max_length=20, default="", blank=True)
    facebook = models.CharField(max_length=20, default="", blank=True)
    twitter = models.CharField(max_length=20, default="", blank=True)
    vk = models.CharField(max_length=20, default="", blank=True)

    followedUsers = models.ManyToManyField('Profile', blank=True)
    followedBlogs = models.ManyToManyField('Blog', blank=True)
    followedPosts = models.ManyToManyField('Post', blank=True)
    
    # Cached

    cachedUserRating = models.IntegerField(default=0, editable=False)

    cachedCommentsNumber = models.PositiveIntegerField(default=0, editable=False)
    cachedPostsNumber = models.PositiveIntegerField(default=0, editable=False)

    cachedSubscriptionsForPostNumber = models.PositiveIntegerField(default=0, editable=False)
    cachedSubscriptionsForBlogNumber = models.PositiveIntegerField(default=0, editable=False)
    cachedSubscriptionsForUserNumber = models.PositiveIntegerField(default=0, editable=False)

    cachedFollowersNumber = models.PositiveIntegerField(default=0, editable=False)

    def recache(self):
        self.cachedUserRating = Post.objects.all().filter(author__profile=self).aggregate(rating=Coalesce(Sum('cachedRating'), Value(0)))['rating'] + Comment.objects.all().filter(author__profile=self).aggregate(rating=Coalesce(Sum('cachedRating'), Value(0)))['rating']

        self.cachedCommentsNumber = Comment.objects.all().filter(author__profile=self).count()
        self.cachedPostsNumber = Post.objects.all().filter(author__profile=self).count()

        self.cachedSubscriptionsForPostNumber = self.followedPosts.count()
        self.cachedSubscriptionsForBlogNumber = self.followedBlogs.count()
        self.cachedSubscriptionsForUserNumber = self.followedUsers.count()

        self.cachedFollowersNumber = Profile.objects.all().filter(followedUsers__in=[self]).count()

        self.save()

    # JSON

    def is_followed_by(self, user):
        result = '0'

        if user.is_authenticated() and Profile.objects.filter(user=user).count() > 0:
            profile = Profile.objects.get(user=user)
            if profile.followedUsers.filter(id=self.id).count() > 0:
                result = '1'

        return result


    def to_JSON(self, user):
        return { 'username' : self.user.username,
                 'firstname' : self.user.first_name,
                 'lastname' : self.user.last_name,

                 'registeredDate' : self.user.date_joined.isoformat(),
                 'last_login' : self.user.last_login.isoformat(),

                 'is_subscribed' : self.is_followed_by(user),

                 'image' : self.image.url if self.image else "",

                 'dateOfBirth' : self.dateOfBirth,
                 'gender' : self.gender,
                 'country' : self.country,
                 'city' : self.city,
                 'facebook' : self.facebook,
                 'twitter' : self.twitter,
                 'vk' : self.vk,

                 'cachedUserRating' : self.cachedUserRating,

                 'cachedCommentsNumber' : self.cachedCommentsNumber,
                 'cachedPostsNumber' : self.cachedPostsNumber,

                 'cachedSubscriptionsForPostNumber' : self.cachedSubscriptionsForPostNumber,
                 'cachedSubscriptionsForBlogNumber' : self.cachedSubscriptionsForBlogNumber,
                 'cachedSubscriptionsForUserNumber' : self.cachedSubscriptionsForUserNumber,

                 'cachedFollowersNumber' : self.cachedFollowersNumber,

                 'id' : self.id }

    def __str__(self):
        return self.user.username
