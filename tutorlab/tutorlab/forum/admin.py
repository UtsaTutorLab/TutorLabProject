from django.contrib import admin
from .models import Post, Comment, Vote, Bookmark, Flag

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    model = Post
    extra = 0
    inlines = [
        CommentInLine
    ]

admin.site.register(Vote)
admin.site.register(Bookmark)
admin.site.register(Flag)
admin.site.register(Post, PostAdmin)
