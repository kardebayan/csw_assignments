from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status', 'tag_list']
    list_filter = ['status', 'created', 'publish', 'author', 'tags']
    search_fields = ['title', 'body', 'tags__name']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', '-publish']
    show_facets = admin.ShowFacets.ALWAYS

    @admin.display(description='Tags')
    def tag_list(self, obj):
        return ', '.join(obj.tags.names())

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
