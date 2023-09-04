from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from .models import Author, Post
from django.db.models import F, Count, Max
from datetime import datetime
# Create your views here.
