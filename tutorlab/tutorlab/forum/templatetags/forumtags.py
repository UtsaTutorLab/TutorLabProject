from django import template
from django.contrib.auth.models import Group
from forum.models import Post
import re

register = template.Library()

@register.filter
def messageformat(string):
    string_list = re.split('<code>', string)
    return string_list


@register.filter
def likebuttonformat(qs, comment_id):
    for c_vote in qs:
        if c_vote.comment.id == comment_id:
            if c_vote.value == 1:
                return 1
            elif c_vote.value == -1:
                return -1
            else:
                return 0

@register.filter
def getgroup(post):
    user = post.user
    group = Group.objects.all()
    for g in group:
        if g in user.groups.all():
            return g

@register.filter
def getrange(total, current):
    if total > 5:
        first = current-2
        if first < 1:
            first = 1
        last = first+4
        if last > total:
            last = total
        first = last-4
        return range(first, last+1)
    return range(1,total+1)

@register.filter
def getactive(active, tab):
    if active == tab:
        return "active"
    else:
        return ""

@register.filter
def mod(number, modby):
    return number % modby
