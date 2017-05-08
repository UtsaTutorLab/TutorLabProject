from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=125, null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    title = models.CharField(max_length=100)
    course_number = models.DecimalField(max_digits=7, decimal_places=3)
    message = models.TextField(max_length=1000)
    view_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    vote_num = models.IntegerField(default=0)
    flag_num = models.IntegerField(default=0)
    protected = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    message = models.TextField(max_length=1000)
    vote_num = models.IntegerField(default=0)

    def __str__(self):
        return self.message

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forum_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + " " + str(self.post)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    value = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

class Flag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.user)