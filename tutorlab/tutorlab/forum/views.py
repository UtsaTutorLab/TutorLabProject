from django.db.models import Q
from django.conf import settings 
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from pusher import pusher
from .models import Post, Comment, Vote, Bookmark, Flag
import json, re


# HOME VIEW
def forum(request):
    if request.user.is_active:
        # recent post Paginator
        post_list = Post.objects.order_by('-date_created')
        recent_paginator = Paginator(post_list, 25) # Show 25 contacts per page
        recent_page = request.GET.get('recent-page')
        try:
            recent_posts = recent_paginator.page(recent_page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            recent_posts = recent_paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            recent_posts = recent_paginator.page(recent_paginator.num_pages)

        # past post Paginator
        past_list = Post.objects.filter(user=request.user).order_by('-date_created')
        past_paginator = Paginator(past_list, 25) # Show 25 contacts per page
        past_page = request.GET.get('past-page')
        try:
            past_posts = past_paginator.page(past_page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            past_posts = past_paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            past_posts = past_paginator.page(past_paginator.num_pages)

        # popular list Paginator
        pop_post_list = Post.objects.order_by('-vote_num')
        pop_paginator = Paginator(pop_post_list, 25) # Show 25 contacts per page
        pop_page = request.GET.get('popular-page')
        try:
            pop_posts = pop_paginator.page(pop_page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            pop_posts = pop_paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            pop_posts = pop_paginator.page(pop_paginator.num_pages)
        
        # bookmarked post Paginator
        book_list = Bookmark.objects.filter(user=request.user)
        post_id = [book.post.id for book in book_list]
        booked_list = Post.objects.filter(id__in=post_id)
        book_paginator = Paginator(booked_list, 25) # Show 25 contacts per page
        book_page = request.GET.get('booked-page')
        try:
            booked_posts = book_paginator.page(book_page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            booked_posts = book_paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            booked_posts = book_paginator.page(book_paginator.num_pages)
        
        if not recent_page is None:
            active_page = 1
        elif not pop_page is None:
            active_page = 2
        elif not past_page is None:
            active_page = 3
        elif not book_page is None:
            active_page = 4
        else:
            active_page = 1

        context = {
            'post_list':recent_posts,
            'past_list':past_posts,
            'popular_list':pop_posts,
            'bookmark_list':booked_posts,
            'active_page':active_page,
        }
        return render(request, "forum/forum_home.html", context)
    else:
        return render(request, "forum/forum_not_loggedin.html")

# AJAX FORUM SEARCH
def forum_search(request):
    if request.method == "GET":
        search_text = request.GET['search_text']
        if search_text is not None and search_text != u"":
            search_text = request.GET['search_text']
            post_results = Post.objects.filter(
                Q(title__icontains=search_text) |
                Q(course_number__icontains=search_text) |
                Q(message__icontains=search_text)
            )
        else: 
            post_results = None

        if search_text is not None and search_text != u"":
            search_text = request.GET['search_text']
            comment_results = Comment.objects.filter(
                Q(message__icontains=search_text)
            )
        else: 
            comment_results = None

        return render(request, 'forum/includes/ajax_forum_search.html', {'post_results':post_results, 'comment_results':comment_results})


# POST PAGE VIEW
def post_view(request, slug, id):
    if request.user.is_active:
        if request.method == "GET":
            try:
                comment_filter = request.GET.get('comment-filter')
                if comment_filter is None:
                    comment_filter = 'date_created'
                post = Post.objects.get(slug=slug, id=id)
                # if comment_filter:
                comments = Comment.objects.filter(post=post).order_by(comment_filter)
                # else:
                #     comments = Comment.objects.filter(post=post).order_by('date_created')
                
                try:
                    vote = get_object_or_404(Vote, user=request.user, post=post)
                except:
                    vote = None
                try:
                    get_object_or_404(Bookmark,user=request.user, post=post)
                    bookmark = 1
                except:
                    bookmark = 0
                try:
                    get_object_or_404(Flag, user=request.user, post=post)
                    flag = 1
                except:
                    flag = 0

                voted_comments = Vote.objects.filter(user=request.user, post=None)

                context = {
                    'post':post,
                    'comments':comments,
                    'vote':vote,
                    'voted_comments':voted_comments,
                    'bookmark':bookmark,
                    'flag':flag,
                    'comment_filter':comment_filter,
                }
                return render(request, "forum/forum_post_view.html", context)
            except:
                return render(request, "forum/forum_no_post.html")
        elif request.method == "POST":
            pass #post a comment
    else:
        return render(request, "forum/forum_not_loggedin.html")

# AJAX CREATE POST
def create_post(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.user)
            post_title = request.POST.get("post_title")
            post_course = request.POST.get("post_course")
            post_content = request.POST.get("post_content")
            new_post = Post.objects.create(
                user=user,
                slug = slugify(post_title),
                title = post_title,
                course_number = post_course,
                message = post_content)
            new_post.save()
            return HttpResponse(
                json.dumps("true"),
                content_type="application/json"
            )
        except:
            return HttpResponse(
                json.dumps("false"),
                content_type="application/json"
            )
    else:
        return 'get'

# AJAX INCREASE POST VIEW COUNT 
def increase_view_count(request):
    if request.method == "POST":
        try:
            post_id = request.POST.get('id')
            post = Post.objects.get(id=post_id)
            if request.user == post.user:
                return HttpResponse(
                json.dumps("can't increase your own view count'"),
                content_type="application/json"
            )
            else:
                post.view_num+=1
                post.save()
                return HttpResponse(
                    json.dumps("true"),
                    content_type="application/json"
                )
        except:
            return HttpResponse(
                json.dumps("could not increase count"),
                content_type="application/json"
            )
    else:
        return HttpResponse(
                json.dumps("GET"),
                content_type="application/json"
            )

#AJAX VOTE ON POST
def vote_post(request):
    if request.user.is_active:
        if request.method == "POST":
            try:
                value = int(request.POST.get('value'))
                post_id = int(request.POST.get('post_id'))
                user = get_object_or_404(User, username=request.user)
                post = get_object_or_404(Post, id=post_id)
                try:
                    vote = get_object_or_404(Vote, user=user, post=post)
                    old_value = vote.value
                    if old_value == value:
                        post.vote_num -= value
                        vote.delete()
                        post.save()
                        return HttpResponse(
                            json.dumps("deleted"),
                            content_type="application/json"
                        )
                    else:
                        vote.value = value
                        post.vote_num += 2*value
                        vote.save()
                        post.save()
                        return HttpResponse(
                            json.dumps("updated"),
                            content_type="application/json"
                        )
                except:
                    vote = Vote.objects.create(
                        user=user,
                        post=post,
                        value=value)
                    post.vote_num += value
                    vote.save()
                    post.save()
                    return HttpResponse(
                        json.dumps("created"),
                        content_type="application/json"
                    )
            except:
                return HttpResponse(
                    json.dumps("invalid"),
                    content_type="application/json"
                )
        else: 
            return HttpResponse(
                    json.dumps("get"),
                    content_type="application/json"
                )
    else:
        return HttpResponse(
                json.dumps("not active user"),
                content_type="application/json"
            )

# AJAX BOOKMARK POST
def bookmark_post(request):
    if request.user.is_active:
        if request.method == "POST":
            try:
                post_id = request.POST.get('post_id')
                user = User.objects.get(username=request.user)
                post = Post.objects.get(id=post_id)
                try:
                    bookmark = Bookmark.objects.get(
                        user=user,
                        post=post)
                    bookmark.delete()
                    return HttpResponse(
                            json.dumps("deleted"),
                            content_type="application/json"
                        )
                except:
                    bookmark = Bookmark.objects.create(
                        user=user,
                        post=post)
                    bookmark.save()
                    return HttpResponse(
                            json.dumps("created"),
                            content_type="application/json"
                        )
            except:
                return HttpResponse(
                        json.dumps("false"),
                        content_type="application/json"
                    )
        else:
            return HttpResponse(
                    json.dumps("get"),
                    content_type="application/json"
                )
    else:
        return HttpResponse(
                json.dumps("not active"),
                content_type="application/json"
            )

# AJAX FLAG POST
def flag_post(request):
    if request.user.is_active:
        if request.method == "POST":
            post_id = request.POST.get('post_id')
            user = User.objects.get(username=request.user)
            post = Post.objects.get(id=post_id)
            try:
                flag = Flag.objects.get(
                    user=user,
                    post=post
                )
                post.flag_num -= 1
                post.save()
                flag.delete()
                return HttpResponse(
                        json.dumps("deleted"),
                        content_type="application/json"
                    )
            except:
                flag = Flag.objects.create(
                    user=user,
                    post=post)
                post.flag_num += 1
                post.save()
                flag.save()
                if post.flag_num >= 5:
                    post.delete()
                    # Send messgae to user their post was flagged and deleted
                    # more that 3 flagged posts and forum account is suspended
                    if user.student.forum_flag_count >= 3:
                        print("deactivate forum permissions")
                        # do this but only for forum
                        # user.is_active = False
            return HttpResponse(
                    json.dumps("created"),
                    content_type="application/json"
                )
        else:
            return HttpResponse(
                    json.dumps("get"),
                    content_type="application/json"
                )
    else:
        return HttpResponse(
                json.dumps("not active"),
                content_type="application/json"
            )

# AJAX CREATE COMMENT
def create_comment(request):
    if request.user.is_active:
        if request.method == "POST":
            try:
                # Initialize pusher
                # does not work either
                pusher_client = pusher.Pusher(
                    app_id=settings.PUSHER_APP_ID,
                    key=settings.PUSHER_KEY,
                    secret=settings.PUSHER_SECRET)
                comment = request.POST.get('comment_message')
                if comment == "" or comment == None:
                    return HttpResponse(
                        json.dumps("false1"),
                        content_type="application/json"
                    )
                post_id = request.POST.get('post_id')
                user = User.objects.get(username=request.user)
                post = Post.objects.get(id=post_id)
                post.comment_num+=1
                post.save()
                new_comment = Comment.objects.create(
                    user=user,
                    post = post,
                    message = comment)
                new_comment.save()
                pusher_client.trigger(u'comments', u'new', {})
                return HttpResponse(
                    json.dumps("true"),
                    content_type="application/json"
                )
            except:
                return HttpResponse(
                    json.dumps("false2"),
                    content_type="application/json"
                 )
        else:
            return HttpResponse(
                json.dumps("get"),
                content_type="application/json"
            )
    else:
        return render(request, "forum/forum_not_loggedin.html")

# AJAX VOTE ON COMMENT
def vote_comment(request):
    if request.user.is_active:
        if request.method == "POST":
            try:
                value = int(request.POST.get('value'))
                comment_id = int(request.POST.get('comment_id'))
                user = get_object_or_404(User, username=request.user)
                comment = get_object_or_404(Comment, id=comment_id)
                try:
                    vote = get_object_or_404(Vote, user=user, comment=comment)
                    old_value = vote.value
                    if old_value == value:
                        comment.vote_num -= value
                        vote.delete()
                        comment.save()
                        return HttpResponse(
                            json.dumps("deleted"),
                            content_type="application/json"
                        )
                    else:
                        vote.value = value
                        comment.vote_num += 2*value
                        vote.save()
                        comment.save()
                        return HttpResponse(
                            json.dumps("updated"),
                            content_type="application/json"
                        )
                except:
                    vote = Vote.objects.create(
                        user=user,
                        comment = comment,
                        value = value)
                    comment.vote_num += value
                    vote.save()
                    comment.save()
                    return HttpResponse(
                        json.dumps("created"),
                        content_type="application/json"
                    )
            except:
                return HttpResponse(
                    json.dumps("invalid"),
                    content_type="application/json"
                )
        else: 
            return HttpResponse(
                    json.dumps("get"),
                    content_type="application/json"
                )
    else:
        return HttpResponse(
                json.dumps("not active user"),
                content_type="application/json"
            )
