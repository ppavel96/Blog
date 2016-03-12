from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    blog = models.CharField(max_length=200)

    title = models.CharField(max_length=200)
    HTMLContent = models.TextField()

    publishedDate = models.DateTimeField(blank=True, null=True)

    rating = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)

    def getDict(self):
        return { 'author' : self.author.username,
                 'blog' : self.blog,
                 'title' : self.title,
                 'HTMLContent' : self.HTMLContent,
                 'publishedDate' : self.publishedDate.isoformat(),
                 'rating' : self.rating,
                 'comments' : self.comments,
                 'id' : self.id }

    def publish(self):
        self.publishedDate = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    avatar = models.CharField(max_length=200)
    publishedDate = models.DateTimeField(blank=True, null=True)

    members = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0)

    def getDict(self):
        return { 'title' : self.title,
                 'description' : self.description,
                 'avatar' : self.avatar,
                 'publishedDate' : self.publishedDate.isoformat(),
                 'members' : self.members,
                 'posts' : self.posts,
                 'id' : self.id }

    def publish(self):
        self.publishedDate = timezone.now()
        self.save()

    def __str__(self):
        return self.title
