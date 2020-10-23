from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(blog)
class blogpost(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'created')
    list_filter = ('title', 'slug', 'author', 'publish', 'created')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(blogComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


@admin.register(Sermons)
class Sermons(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'created')
    list_filter = ('title', 'slug', 'author', 'publish', 'created')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(SermonsComment)
class SermonsCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


@admin.register(Events)
class Events(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'created')
    list_filter = ('title', 'slug', 'author', 'publish', 'created')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Services)
class Events(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'created')
    list_filter = ('title', 'slug', 'author', 'publish', 'created')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(EventComment)
class EventCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


#
# @admin.register(Services)
# class ServicesAdmin(admin.ModelAdmin):
#     list_display = ('user', 'service', 'Description', 'created')
#     # list_filter = ('active', 'created', 'updated')
#     search_fields = ('user', 'service', 'created')


@admin.register(Quotes)
class QuotesAdmin(admin.ModelAdmin):
    list_display = ('user', 'bibleverse', 'speaker', 'created')
    # list_filter = ('active', 'created', 'updated')
    search_fields = ('user', 'bibleverse', 'created')


@admin.register(Mtu)
class MtuAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'joined', 'body', 'number')
    # list_filter = ('active', 'created', 'updated')
    search_fields = ('user', 'name', 'joined')
