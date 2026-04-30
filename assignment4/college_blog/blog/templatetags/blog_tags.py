import markdown

from django import template
from django.db.models import Count, Q
from django.utils.safestring import mark_safe

from ..models import Post


register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


def _published_posts_for_tag(tag=None):
    posts = Post.published.all()
    if tag:
        posts = posts.filter(tags__in=[tag]).distinct()
    return posts


@register.inclusion_tag('blog/post/latest/list.html')
def show_latest_posts(count=5, tag=None):
    latest_posts = _published_posts_for_tag(tag).order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('blog/post/most_commented/list.html')
def show_most_commented_posts(count=5, tag=None):
    most_commented_posts = (
        _published_posts_for_tag(tag)
        .annotate(
            total_comments=Count('comments', filter=Q(comments__active=True))
        )
        .order_by('-total_comments', '-publish')[:count]
    )
    return {'most_commented_posts': most_commented_posts}


@register.filter(name='markdown_format')
def markdown_format(text):
    return mark_safe(markdown.markdown(text or '', extensions=['extra']))
