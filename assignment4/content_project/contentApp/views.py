from django.db import connection
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from taggit.models import Tag

from .models import Article


class ArticleSearchView(ListView):
    context_object_name = 'articles'
    paginate_by = 5
    template_name = 'contentApp/article/search.html'

    def get_queryset(self):
        self.query = self.request.GET.get('q', '').strip()
        queryset = Article.published.select_related('author').prefetch_related('tags')

        if not self.query:
            return queryset.none()

        if connection.vendor == 'postgresql':
            from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

            vector = (
                SearchVector('title', weight='A', config='english')
                + SearchVector('body', weight='B', config='english')
            )
            search_query = SearchQuery(self.query, search_type='websearch', config='english')
            return (
                queryset.annotate(search=vector, rank=SearchRank(vector, search_query))
                .filter(search=search_query)
                .order_by('-rank', '-publish')
            )

        return (
            queryset.filter(
                Q(title__icontains=self.query)
                | Q(body__icontains=self.query)
                | Q(tags__name__icontains=self.query)
            )
            .distinct()
            .order_by('-publish')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        context['is_postgres_search'] = connection.vendor == 'postgresql'
        return context


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
