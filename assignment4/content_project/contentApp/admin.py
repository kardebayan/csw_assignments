from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status', 'tag_list']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body', 'tags__name']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', '-publish']

    @admin.display(description='Tags')
    def tag_list(self, obj):
        return ', '.join(obj.tags.names())
