from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)


class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('followedUsers', 'followedPosts', 'followedBlogs',)


admin.site.register(Post, PostAdmin)
admin.site.register(Blog)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(VoteForPost)
admin.site.register(VoteForComment)
