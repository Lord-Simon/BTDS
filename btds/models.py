from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

# Create your models here.

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
    link = models.CharField(max_length=500)
    def __unicode__(self):
        return self.name

class Editor(models.Model):
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=500)
    def __unicode__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length = 255)
    iso = models.SlugField(max_length=2, unique=True)
    def __unicode__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length = 255)
    link = models.CharField(max_length=500)
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
    synopsis = models.TextField()
    def __unicode__(self):
        return self.name

class Volume(models.Model):
    name = models.CharField(max_length=255, blank=True)
    number = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    novel = models.ForeignKey(Novel)
    synopsis = models.TextField()
    isbn = models.CharField(max_length=17, blank=True)
    year = models.PositiveSmallIntegerField(max_length=4)
    def __unicode__(self):
        return self.volume +':'+ str(self.number)

class Link(models.Model):
    link = models.CharField(max_length=500)
    FILE_FORMATS = (
        ('p','PDF'),
        ('e','ePUB'),
        ('m','MOBI'),
    )
    format = models.CharField(max_length=1, choices=FILE_FORMATS)
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
    link = models.ManyToManyField(Link)
    translator = models.ManyToManyField(Translator)
    editor = models.ManyToManyField(Editor)
    genre = models.ManyToManyField(Genre)
    publisher = models.ForeignKey(Publisher)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def uuid_gen():
        return uuid4()
    uuid = models.SlugField(max_length=36, unique=True, default=uuid_gen)
    def __unicode__(self):
        return self.bt_title
