from django import template
from django.db.models import Count, Q

from ..models import Post


register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest/list.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('blog/post/most_commented/list.html')
def show_most_commented_posts(count=5):
    most_commented_posts = (
        Post.published.annotate(
            total_comments=Count('comments', filter=Q(comments__active=True))
        )
        .order_by('-total_comments', '-publish')[:count]
    )
    return {'most_commented_posts': most_commented_posts}
