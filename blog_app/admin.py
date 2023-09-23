from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from . import models
from django.db.models import Count
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse
# Register your models here.


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    """ It is responsible for Post admin """
    list_display = ['title', 'date', 'author_name',
                    'comment_count', 'tag_count']
    list_per_page = 10
    ordering = ['-date', 'title']
    exclude = ['picture']
    search_fields = ['title__istartswith', 'author__name__istartswith']
    list_filter = ['date', 'tag']

    @admin.display(description='Total Comments', ordering='comment_count')
    def comment_count(self, post):
        """ Calculating comment count on this post """
        return post.comment_count

    @admin.display(description='author name')
    def author_name(self, post):
        """ Providing author name """
        return post.author.name

    @admin.display(description='Total tags', ordering='tag_count')
    def tag_count(self, post):
        """ Calculating tag count on this post """
        url = reverse('admin:blog_app_tag_changelist') + \
            '?' + urlencode({'post__id': post.id})
        html = format_html(
            '<a href="{}">{}</a>', url, post.tag_count)
        if post.tag_count == 0:
            return post.tag_count
        return html

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(comment_count=Count('comment'), tag_count=Count('tag', distinct=True)).select_related('author')


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    """ It is responsible for Author admin """
    list_display = ['name', 'joined_on', 'published']
    list_per_page = 10
    list_filter = ['joined_on']
    ordering = ['-joined_on']
    exclude = ['picture']
    search_fields = ['name__istartswith']

    @admin.display(description='Total posts', ordering='post_count')
    def published(self, author):
        """ calculating an author published post count """
        url = reverse('admin:blog_app_post_changelist') + \
            '?' + urlencode({'author__id': author.id})
        html = format_html(
            '<a href="{}">{}</a>', url, author.post_count)
        if author.post_count == 0:
            return author.post_count
        return html

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(post_count=Count('post'))


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    """ It is responsible for Tag admin """
    list_display = ['label', 'post_count']
    search_fields = ['label__istartswith']

    @admin.display(description='Total posts', ordering='post_count')
    def post_count(self, tag):
        """ Calculating post count """
        return tag.post_count

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(post_count=Count('post'))
