from django.conf.urls import url, include
from . import views

app_name = 'forum'
urlpatterns = [
    url(r'^$', views.forum, name='forum'),
    url(r'ajax-bookmark-post/$', views.bookmark_post, name='ajax_bookmark_post'),
    url(r'ajax-create-post/$', views.create_post, name='ajax_create_post'),
    url(r'ajax-create-comment/$', views.create_comment, name='ajax_create_comment'),
    url(r'ajax-flag-post/$', views.flag_post, name='ajax_flag_post'),
    url(r'ajax-forum-search/$', views.forum_search, name='ajax_forum_search'),
    url(r'ajax-increase-view-count/$', views.increase_view_count, name='ajax_increase_view_count'),
    url(r'ajax-vote-comment/$', views.vote_comment, name='ajax_vote_comment'),
    url(r'ajax-vote-post/$', views.vote_post, name='ajax_vote_post'),
    url(r'post/(?P<slug>[\w-]+)-(?P<id>\d+)/$', views.post_view, name='post_view'),
]