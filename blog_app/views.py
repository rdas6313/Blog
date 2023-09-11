from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Tag, Author
from django.db.models import Count, Prefetch
# Create your views here.


def index(request):
    """ This function is responsible for index page """
    selected_tag_list = request.GET.getlist('list_params[]')

    posts_queryset = Post \
        .objects \
        .select_related(
            "author") \
        .filter(tag__isnull=False) \
        .distinct() \
        .order_by('-date') \

    latest_post_queryset = posts_queryset

    if selected_tag_list:
        posts_queryset = posts_queryset.filter(tag__in=selected_tag_list)

    tag_queryset = Tag.objects.exclude(post__isnull=True)

    paginator = Paginator(posts_queryset, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    selected_tag_list = [int(i) for i in selected_tag_list]
    context = {
        "posts": page_obj,
        "latest_post": latest_post_queryset[:6],
        "tags": tag_queryset,
        "selected_tags": selected_tag_list
    }
    return render(request, 'blog_app/blog_post_list.html', context)


def author_detail(request, id):
    """ This function is responsible for author detail page """

    selected_tag_list = request.GET.getlist('list_params[]')

    author = get_object_or_404(Author, pk=id)

    author_post_queryset = author.post_set.filter(
        tag__isnull=False).distinct().order_by('-date')

    if selected_tag_list:
        author_post_queryset = author_post_queryset.filter(
            tag__in=selected_tag_list).distinct()

    tags = Tag.objects.filter(post__author=author).distinct()

    paginator = Paginator(author_post_queryset, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    selected_tag_list = [int(i) for i in selected_tag_list]

    context = {
        "posts": page_obj,
        "author": author,
        "tag_title": "Tags",
        "tags": tags,
        "selected_tags": selected_tag_list
    }
    return render(request, 'blog_app/blog_author_detail.html', context)


def post_detail(request, id):
    post_queryset = Post.objects.select_related(
        'author')
    post = get_object_or_404(post_queryset, pk=id)
    author = post.author
    latest_posts = post_queryset[:6]
    context = {
        'post': post,
        'author': author,
        'latest_post': latest_posts
    }
    return render(request, 'blog_app/blog_post_detail.html', context)
