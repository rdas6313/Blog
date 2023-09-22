from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Tag, Author, Comment
from django.db.models import Count, Prefetch, F
from .forms import CommentForm
# Create your views here.


def index(request):
    """ This function is responsible for index page """
    request.session.set_test_cookie()

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


def session_handle(request, comment_id, like, on_cookie_enabled):

    cookie_alert = None
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        request.session.set_expiry(0)
        on_cookie_enabled(request, comment_id, like)
    else:
        cookie_alert = 'Enable cookies! Otherwise some function may not work.'

    request.session.set_test_cookie()
    return cookie_alert


def on_cookie_enabled(request, comment_id, like):

    if comment_id and like:
        session_comment_id = f"comment_{comment_id}"
        prev_comment = request.session.get(session_comment_id, None)
        prev_like = None

        if prev_comment:
            prev_like = prev_comment.get('like', None)

        if like == 'true':

            if prev_like is None:

                Comment.objects.filter(
                    pk=comment_id).update(like=F('like')+1)
                request.session[session_comment_id] = {}
                request.session[session_comment_id]['like'] = True

            elif prev_like:

                Comment.objects.filter(
                    pk=comment_id).update(like=F('like')-1)
                del request.session[session_comment_id]['like']

            else:

                Comment.objects.filter(pk=comment_id).update(
                    like=F('like')+1, dislike=F('dislike')-1)
                request.session[session_comment_id]['like'] = True

        elif like == 'false':

            if prev_like is None:

                Comment.objects.filter(pk=comment_id).update(
                    dislike=F('dislike')+1)
                request.session[session_comment_id] = {}
                request.session[session_comment_id]['like'] = False

            elif prev_like:

                Comment.objects.filter(pk=comment_id).update(
                    dislike=F('dislike')+1, like=F('like')-1)
                request.session[session_comment_id]['like'] = False

            else:

                Comment.objects.filter(pk=comment_id).update(
                    dislike=F('dislike')-1)
                del request.session[session_comment_id]['like']


def post_detail(request, id):

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CommentForm()

    comment_id = request.GET.get('comment', None)
    like = request.GET.get('like', None)
    cookie_alert = session_handle(request, comment_id, like, on_cookie_enabled)

    post_queryset = Post.objects.select_related(
        'author')
    post = get_object_or_404(post_queryset, pk=id)
    author = post.author
    latest_posts = post_queryset[:6]
    comment_set = post.comment_set.order_by('-commented_on')
    context = {
        'post': post,
        'author': author,
        'latest_post': latest_posts,
        'cookie_alert': cookie_alert,
        'comment_set': comment_set,
        'session': request.session,
        'form': form
    }
    return render(request, 'blog_app/blog_post_detail.html', context)
