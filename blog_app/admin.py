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


class TagInline(admin.TabularInline):
    model = models.Tag.post.through
    extra = 0


class PostInline(admin.TabularInline):
    model = models.Post
    extra = 0
    max_num = 3
    min_num = 1


class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 0
    readonly_fields = [
        'like', 'dislike', 'commented_on']


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    """ It is responsible for Post admin """
    list_display = ['title', 'date', 'author_name',
                    'comment_count', 'tag_count',]
    list_per_page = 10
    ordering = ['-date', 'title']
    search_fields = ['title__istartswith', 'author__name__istartswith']
    list_filter = ['date', 'tag']
    readonly_fields = ['date']
    autocomplete_fields = ['author']
    inlines = [TagInline, CommentInline]

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
        qs = super().get_queryset(request).annotate(comment_count=Count('comment'),
                                                    tag_count=Count('tag', distinct=True)).select_related('author')
        if request.user.is_staff and not request.user.is_superuser:
            return qs.filter(author__user=request.user)
        return qs


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    """ It is responsible for Author admin """
    list_display = ['name', 'joined_on', 'published']
    list_per_page = 10
    list_filter = ['joined_on']
    ordering = ['-joined_on']
    search_fields = ['name__istartswith']
    actions = ['delete_posts']
    readonly_fields = ['joined_on']
    exclude = ['user']

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
        qs = super().get_queryset(request).annotate(post_count=Count('post'))
        if request.user.is_staff and not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs

    @admin.action(description='Delete posts from seleted authors')
    def delete_posts(self, request, queryset):
        author_queryset = queryset.prefetch_related('post_set')
        count = 0
        for author in author_queryset:
            ret = author.post_set.all().delete()
            if ret[0] > 0:
                count += 1
        self.message_user(
            request,
            f"{count} author posts were successfully deleted"
        )


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    """ It is responsible for Tag admin """
    list_display = ['label', 'post_count']
    search_fields = ['label__istartswith']
    exclude = ['post']

    @admin.display(description='Total posts', ordering='post_count')
    def post_count(self, tag):
        """ Calculating post count """
        return tag.post_count

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(post_count=Count('post'))


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'commented_on', 'post_name', 'like', 'dislike']
    search_fields = ['name__istartswith',
                     'commented_on', 'post__title__istartswith']
    list_select_related = ['post']

    readonly_fields = ['like', 'dislike']

    def post_name(self, comment):
        url = reverse('admin:blog_app_post_change', args=(comment.post.id,))
        html = format_html('<a href="{}">{}</a>', url, comment.post.title)
        return html

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        if request.user.is_staff and not request.user.is_superuser:
            return super().get_queryset(request).filter(post__author__user=request.user)
        return super().get_queryset(request)
