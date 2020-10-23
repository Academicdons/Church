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
from django.template import loader
from django.http import HttpResponse
from .sharkbot import *
from .bot import *
from .forms import *
import random


def about(request):
    #quotes = Quotes.objects.all().reverse()[:1]
    object_list = Quotes.objects.all()

    paginator = Paginator(object_list, 1)  # 5 posts in each page
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
                  'about.html',
                  {'page': page,
                   'posts': posts})

def contact(request):
    return render(request, 'contact.html')

def home(request):
    name = request.user
    posts = blog.published.all().reverse()[:4]

    sermons = Sermons.published.all().reverse()[:3]

    quotes = Quotes.objects.all().reverse()[:10]
    events = Events.objects.all().reverse()[:3]
    services = Services.objects.all().reverse()[:3]
    template = loader.get_template('index.html')
    context = {'name': name, 'posts': posts, 'sermons': sermons, 'quotes': quotes, 'events': events, 'services': services}

    return HttpResponse(template.render(context, request))


def post_list(request):
    posts = blog.published.all()
    object_list = blog.published.all()

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
                  'news.html',
                  {'page': page,
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
                  'blog_details.html',
                  {'post': post,
                   'comments': comments, 'posts': posts,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


def Sermon_list(request):
    posts = Sermons.published.all()
    object_list = Sermons.published.all()

    paginator = Paginator(object_list, 8)  # 5 posts in each page
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
                  'sermons.html',
                  {'page': page,
                   'posts': posts})


def Sermons_detail(request, year, month, day, post):
    post = get_object_or_404(Sermons, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    posts = Sermons.published.all().reverse()[:3]
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = SermonCommentForm(data=request.POST)
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
                   'sermon_form': comment_form})


def Events_list(request):
    posts = Events.published.all()
    object_list = Events.published.all()

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
                  'events.html',
                  {'page': page,
                   'posts': posts})


def Events_detail(request, year, month, day, post):
    post = get_object_or_404(Events, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    posts = Events.published.all().reverse()[:3]
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = EventsCommentForm(data=request.POST)
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
                  'event_details.html',
                  {'post': post,
                   'comments': comments, 'posts': posts,
                   'new_comment': new_comment,
                   'sermon_form': comment_form})

def bothome(request):
    user = request.user
    name = user.username
    print(name)
    context = {'name': name}
    template = loader.get_template('botindex.html')
    return HttpResponse(template.render(context, request))

def startbotone(request):
    user = request.user
    name = user.username
    ed = EssaySharkBot()
    print("The bot is now starting, there will be no further printing of information")
    ed.init_bot()
    template = loader.get_template('bot2.html')
    context = {'name': name}

    return HttpResponse(template.render(context, request))

def startbottwo(request):
    user = request.user
    name = user.username
    ed = GeeBotPro()
    print("The bot is now starting, there will be no further printing of information")
    ed.init_bot()
    template = loader.get_template('thankyou.html')
    context = {'name': name}

    return HttpResponse(template.render(context, request))
