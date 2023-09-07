from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<int:id>", views.detail, name="post_detail"),
    path("author/<int:id>", views.author_detail, name="author_detail")
]
