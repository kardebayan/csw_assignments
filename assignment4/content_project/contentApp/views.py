from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from taggit.models import Tag

from .models import Article


class ArticleListView(ListView):
    context_object_name = 'articles'
    paginate_by = 5
    template_name = 'contentApp/article/list.html'

    def get_queryset(self):
        queryset = Article.published.all()
        self.tag = None
        tag_slug = self.kwargs.get('tag_slug')

        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[self.tag])

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


def article_detail(request, year, month, day, article):
    article = get_object_or_404(
        Article,
        status=Article.Status.PUBLISHED,
        slug=article,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    article_tags_ids = article.tags.values_list('id', flat=True)
    similar_articles = (
        Article.published.filter(tags__in=article_tags_ids)
        .exclude(id=article.id)
        .annotate(same_tags=Count('tags'))
        .order_by('-same_tags', '-publish')[:4]
    )

    return render(
        request,
        'contentApp/article/detail.html',
        {
            'article': article,
            'similar_articles': similar_articles,
        },
    )
