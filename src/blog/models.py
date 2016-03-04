from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    blog = models.ForeignKey('Blog')

    title = models.CharField(max_length=200)
    text = models.TextField()

    published_date = models.DateTimeField(editable=False, null=True)

    positive = models.PositiveIntegerField(default=0)
    negative = models.PositiveIntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Blog(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
