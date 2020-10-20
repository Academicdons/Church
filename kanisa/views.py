from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger
from .forms import *
import random

def home(request):
    context = {''}
    return render(request, 'index', context)

def post_list(request, tag_slug=None):
    posts = blog.published.all()
    object_list = blog.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 4)  # 5 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blogs_new.html',
                  {'page': page, 'tag': tag,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(blog, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    posts = blog.published.all().reverse()[:3]
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'blogDetails.html',
                  {'post': post,
                   'comments': comments, 'posts': posts,
                   'new_comment': new_comment,
                   'comment_form': comment_form})
