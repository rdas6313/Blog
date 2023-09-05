from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from .models import Author, Post
from django.db.models import F, Count, Max
from datetime import datetime
# Create your views here.


def index(request):
    queryset = Post.objects.select_related("author").all()
    context = {
        "posts": queryset
    }
    return render(request, 'blog_app/blog_post_list.html', context)


def detail(request, id):
    return render(request, 'blog_app/blog_post_detail.html')
