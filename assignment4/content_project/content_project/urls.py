"""
URL configuration for content_project.
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from contentApp.sitemaps import ArticleSitemap


sitemaps = {
    'articles': ArticleSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('', include('contentApp.urls', namespace='contentApp')),
]
