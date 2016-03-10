from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    blog = models.CharField(max_length=200)

    title = models.CharField(max_length=200)
    HTMLContent = models.TextField()

    publishedDate = models.DateTimeField(blank=True, null=True)
    rating = models.PositiveIntegerField(default=0)

    def getDict(self):
        return { 'author' : self.author.username,
                 'blog' : self.blog,
                 'title' : self.title,
                 'HTMLContent' : self.HTMLContent,
                 'publishedDate' : self.publishedDate.isoformat(),
                 'rating' : self.rating }

    def publish(self):
        self.publishedDate = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    avatar = models.CharField(max_length=200)

    created_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
