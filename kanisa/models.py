from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import uuid


# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset() \
            .filter(status='published')


class Mtu(models.Model):
    Designation = (
        ('Pastor', 'Pastor'),
        ('Usher', 'Usher'),
    )
    name = models.CharField(max_length=30)
    number = models.CharField(max_length=30)
    slug = models.SlugField(max_length=250, unique_for_date='joined')
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()
    joined = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    designation = models.CharField(max_length=10, choices=Designation, default='Pastor')
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.
    # tags = TaggableManager()
    image = models.ImageField(null=True, blank=True, upload_to='images/', height_field="image_height",
                              width_field="image_width", editable=True,
                              default='images/NoImageAvailable.png')
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")

    class Meta:
        ordering = ('-joined',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Quotes(models.Model):
    user = models.ForeignKey(Mtu, null=True, blank=True, on_delete=models.CASCADE)
    bibleverse = models.TextField()
    speaker = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.bibleverse


class Services(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(Mtu, on_delete=models.CASCADE, related_name='Services_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.
    # tags = TaggableManager()
    image = models.ImageField(null=True, blank=True, upload_to='images/', height_field="image_height",
                              width_field="image_width", editable=True,
                              default='images/NoImageAvailable.png')
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class blog(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(Mtu, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.
    # tags = TaggableManager()
    image = models.ImageField(null=True, blank=True, upload_to='images/', height_field="image_height",
                              width_field="image_width", editable=True,
                              default='images/NoImageAvailable.png')
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class blogComment(models.Model):
    post = models.ForeignKey(blog,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


class Sermons(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(Mtu, on_delete=models.CASCADE, related_name='sermon_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.
    # tags = TaggableManager()
    image = models.ImageField(null=True, blank=True, upload_to='images/', height_field="image_height",
                              width_field="image_width", editable=True,
                              default='images/NoImageAvailable.png')
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class SermonsComment(models.Model):
    post = models.ForeignKey(Sermons,
                             on_delete=models.CASCADE,
                             related_name='sermoncomments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


class Events(models.Model):
    STATUS_CHOICES = (
        ('Upcoming', 'Upcoming'),
        ('Passed', 'Passed'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(Mtu, on_delete=models.CASCADE, related_name='events_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Upcoming')
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.
    # tags = TaggableManager()
    image = models.ImageField(null=True, blank=True, upload_to='images/', height_field="image_height",
                              width_field="image_width", editable=True,
                              default='images/NoImageAvailable.png')
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class EventComment(models.Model):
    post = models.ForeignKey(Sermons,
                             on_delete=models.CASCADE,
                             related_name='eventcomments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
