from django.contrib.syndication.views import Feed
from django.urls import reverse

from .models import Article


class LatestArticlesFeed(Feed):
    title = 'Content Project'
    link = '/feed/'
    description = 'Latest published articles from Content Project.'

    def items(self):
        return Article.published.all()[:10]

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
            'contentApp:article_detail',
            args=[
                item.publish.year,
                item.publish.month,
                item.publish.day,
                item.slug,
            ],
        )
