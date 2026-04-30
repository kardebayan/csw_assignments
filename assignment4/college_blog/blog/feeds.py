from django.contrib.syndication.views import Feed
from django.urls import reverse

from .models import Post


class LatestPostsFeed(Feed):
    title = 'My Blog'
    link = '/feed/'
    description = 'Latest published posts from My Blog.'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_pubdate(self, item):
        return item.publish

    def item_updateddate(self, item):
        return item.updated

    def item_author_name(self, item):
        return item.author.get_username()

    def item_link(self, item):
        return reverse(
            'blog:post_detail',
            args=[
                item.publish.year,
                item.publish.month,
                item.publish.day,
                item.slug,
            ],
        )
