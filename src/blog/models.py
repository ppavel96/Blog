from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    blog = models.ForeignKey('Blog')

    title = models.CharField(max_length=200)
    content = models.TextField()

    publishedDate = models.DateTimeField(blank=True, null=True)

    tags = models.ManyToManyField('Tag', blank=True)

    # Cached

    cachedRating = models.PositiveIntegerField(default=0, editable=False)
    cachedCommentsNumber = models.PositiveIntegerField(default=0, editable=False)
    cachedSubscriptionsNumber = models.PositiveIntegerField(default=0, editable=False)

    # JSON

    def to_JSON(self):
        tags = list()
        for i in self.tags.all():
            tags.append(i.__str__())

        return { "author" : self.author.username,
                 "blog" : self.blog.__str__(),

                 "title" : self.title,
                 "content" : self.content,

                 "publishedDate" : self.publishedDate.isoformat(),

                 "tags" : tags,

                 "cachedRating" : self.cachedRating,
                 "cachedCommentsNumber" : self.cachedCommentsNumber,
                 "cachedSubscriptionsNumber" : self.cachedSubscriptionsNumber,

                 "id" : self.id }

    # Publish

    def publish(self):
        self.publishedDate = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class VoteForPost(models.Model):
    user = models.ForeignKey('auth.User')
    post = models.ForeignKey('Post')
    like = models.NullBooleanField()


class Tag(models.Model):
    name = models.CharField(max_length=10)

    # Cached

    cachedTagNumber = models.PositiveIntegerField(default=0, editable=False)


    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey('auth.User')
    post = models.ForeignKey('Post')

    content = models.TextField()

    publishedDate = models.DateTimeField(blank=True, null=True)

    # Comment Path (up to 5 levels)

    path0 = models.PositiveIntegerField(default=0)
    path1 = models.PositiveIntegerField(default=0, null=True)
    path2 = models.PositiveIntegerField(default=0, null=True)
    path3 = models.PositiveIntegerField(default=0, null=True)
    path4 = models.PositiveIntegerField(default=0, null=True)
    
    # Cached

    cachedRating = models.PositiveIntegerField(default=0)

    # JSON

    def to_JSON(self):
        return { 'author' : self.author.username,
                 'post' : self.post,

                 'content' : self.content,

                 'publishedDate' : self.publishedDate.isoformat(),

                 'path0' : self.path0,
                 'path1' : self.path1,
                 'path2' : self.path2,
                 'path3' : self.path3,
                 'path4' : self.path4,

                 'cachedRating' : self.cachedRating,

                 'id' : self.id }

    # Publish

    def publish(self):
        self.publishedDate = timezone.now()
        self.save()


class VoteForComment(models.Model):
    user = models.ForeignKey('auth.User')
    comment = models.ForeignKey('Comment')
    like = models.NullBooleanField()


class Blog(models.Model):
    creator = models.ForeignKey('auth.User')

    title = models.CharField(max_length=200)
    image = models.CharField(max_length=200, blank=True)

    description = models.TextField()

    publishedDate = models.DateTimeField(blank=True, null=True)

    # Cached

    cachedBlogRating = models.PositiveIntegerField(default=0, editable=False)
    cachedMembersNumber = models.PositiveIntegerField(default=0, editable=False)
    cachedPostsNumber = models.PositiveIntegerField(default=0, editable=False)

    # JSON

    def to_JSON(self):
        return { 'creator' : self.creator.username,

                 'title' : self.title,
                 'image' : self.image,

                 'description' : self.description,

                 'publishedDate' : self.publishedDate.isoformat(),

                 'cachedBlogRating' : self.cachedBlogRating,
                 'cachedMembersNumber' : self.cachedMembersNumber,
                 'cachedPostsNumber' : self.cachedPostsNumber,

                 'id' : self.id }

    def publish(self):
        self.publishedDate = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    image = models.CharField(max_length=200, blank=True)

    dateOfBirth = models.DateField()

    followedUsers = models.ManyToManyField('Profile', blank=True)
    followedBlogs = models.ManyToManyField('Blog', blank=True)
    followedPosts = models.ManyToManyField('Post', blank=True)
    
    # Cached

    cachedUserRating = models.PositiveIntegerField(default=0, editable=False)

    cachedCommentsNumber = models.PositiveIntegerField(default=0, editable=False)
    cachedPostsNumber = models.PositiveIntegerField(default=0, editable=False)

    cachedSubscriptionsForPostNumber = models.PositiveIntegerField(default=0, editable=False)
    cachedSubscriptionsForBlogNumber = models.PositiveIntegerField(default=0, editable=False)
    cachedSubscriptionsForUserNumber = models.PositiveIntegerField(default=0, editable=False)

    cachedFollowersNumber = models.PositiveIntegerField(default=0, editable=False)

    # JSON

    def to_JSON(self):
        return { 'username' : self.user.username,
                 'firstName' : self.user.first_name,
                 'lastName' : self.user.last_name,

                 'image' : self.image,

                 'dateOfBirth' : self.dateOfBirth.isoformat(),

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
