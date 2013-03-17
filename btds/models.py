from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

# Create your models here.

FILE_FORMATS = (
    ('p','PDF'),
    ('e','ePUB'),
    ('m','MOBI'),
)

class Author(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class Illustrator(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class Translator(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=500, blank=True)
    def __unicode__(self):
        return self.name

class Editor(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=500, blank=True)
    def __unicode__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length = 255)
    iso = models.SlugField(max_length=2, unique=True)
    def __unicode__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length = 255)
    link = models.URLField(max_length=500, blank=True)
    def __unicode__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length = 255)
    def __unicode__(self):
        return self.name

class Novel(models.Model):
    name = models.CharField(max_length=255, blank=False)
    illustrator = models.ForeignKey(Illustrator)
    author = models.ForeignKey(Author)
    synopsis = models.TextField(blank=True)
    def get_absolute_url(self):
      return ('btds.views.series',(),{'sid':self.pk})
    def __unicode__(self):
        return self.name

class Volume(models.Model):
    name = models.CharField(max_length=255, blank=True)
    number = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    novel = models.ForeignKey(Novel)
    synopsis = models.TextField(blank=True)
    isbn = models.CharField(max_length=17, blank=True)
    year = models.PositiveSmallIntegerField(max_length=4)
    def get_absolute_url(self):
      return ('btds.views.volume',(),{'bid':self.pk})
    def __unicode__(self):
        return self.novel.name +' - '+str(self.number) +' - '+ self.name

class Link(models.Model):
    link = models.URLField(max_length=500)
    file_format = models.CharField(max_length=1, choices=FILE_FORMATS)
    user = models.ForeignKey(User)
    visible = models.BooleanField(default=False)
    protected = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.link

class Meta(models.Model):
    bt_title = models.CharField(max_length=255, blank=True)
    generate_epub = models.BooleanField(default=False)
    link = models.ManyToManyField(Link, blank=True, null=True)
    translator = models.ManyToManyField(Translator, blank=True, null=True)
    editor = models.ManyToManyField(Editor, blank=True, null=True)
    genre = models.ManyToManyField(Genre, blank=True, null=True)
    publisher = models.ForeignKey(Publisher, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    uuid = models.SlugField(max_length=36, unique=True, default=uuid4())
    def __unicode__(self):
        return self.bt_title

class Image(models.Model):
    volume = models.ForeignKey(Volume)
    image = models.ImageField(upload_to = 'images')
    cover = models.BooleanField(default=False)
    info = models.TextField(blank=True)