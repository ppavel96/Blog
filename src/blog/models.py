from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    blog = models.CharField(max_length=200)

    title = models.CharField(max_length=200)
    html_content = models.TextField()

    published_date = models.DateTimeField(blank=True, null=True)
    rating = models.PositiveIntegerField(default=0)

    def get_dict(self):
        return { 'author' : self.author.username,
                 'blog' : self.blog,
                 'title' : self.title,
                 'html_content' : self.html_content,
                 'published_date' : self.published_date,
                 'rating' : self.rating }

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
