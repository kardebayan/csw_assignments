from django.urls import path

from . import views
from .feeds import LatestArticlesFeed


app_name = 'contentApp'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('feed/', LatestArticlesFeed(), name='article_feed'),
    path('search/', views.ArticleSearchView.as_view(), name='article_search'),
    path('tag/<slug:tag_slug>/', views.ArticleListView.as_view(), name='article_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:article>/', views.article_detail, name='article_detail'),
]
