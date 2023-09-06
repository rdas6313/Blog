from django.shortcuts import render
from .models import Post, Tag

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

    context = {
        "posts": list(posts_queryset),
        "latest_post": posts_queryset[:6],
        "latest_tags": tags_queryset
    }
    return render(request, 'blog_app/blog_post_list.html', context)


def detail(request, id):
    return render(request, 'blog_app/blog_post_detail.html')
