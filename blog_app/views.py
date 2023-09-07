from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Tag, Author

# Create your views here.


def index(request):
    """ This function is responsible for index page """
    posts_queryset = Post \
        .objects \
        .select_related(
            "author") \
        .all() \
        .order_by('-date')

    tags_queryset = Tag.objects.filter(post__in=posts_queryset).distinct()

    paginator = Paginator(posts_queryset, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "posts": page_obj,
        "latest_post": posts_queryset[:6],
        "tags": tags_queryset
    }
    return render(request, 'blog_app/blog_post_list.html', context)


def author_detail(request, id):
    """ This function is responsible for author detail page """

    author = get_object_or_404(Author, pk=id)
    author_post_queryset = author.post_set.prefetch_related(
        'tag_set').order_by('-date')

    tag_list = []
    for post in author_post_queryset:
        for tag in post.tag_set.all():
            tag_list.append(tag)

    tags = set(tag_list)

    paginator = Paginator(author_post_queryset, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "posts": page_obj,
        "author": author,
        "tag_title": "Tags",
        "tags": tags
    }
    return render(request, 'blog_app/blog_author_detail.html', context)


def detail(request, id):
    return render(request, 'blog_app/blog_post_detail.html')
