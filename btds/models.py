from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from uuid import uuid4
import itertools
import os

# Create your models here.

PUBLISHER_TYPE = (
    ('m','MediaWiki'),
    ('w','WordPress'),
    ('b','BlogSpot'),
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
    link = models.URLField(max_length=500, blank=True, null=True)
    def __unicode__(self):
        return self.name

class Editor(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=500, blank=True, null=True)
    def __unicode__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length = 255)
    iso = models.SlugField(max_length=2, unique=True)
    def __unicode__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length = 255)
    publisher_type = models.CharField(max_length=1, choices=PUBLISHER_TYPE)
    link = models.URLField(max_length=500, blank=True, null=True)
    def __unicode__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length = 255)
    def __unicode__(self):
        return self.name

class Format(models.Model):
    name = models.CharField(max_length = 5)
    def __unicode__(self):
        return self.name

class Novel(models.Model):
    name = models.CharField(max_length=255, blank=False)
    genre = models.ManyToManyField(Genre, blank=True, null=True)
    illustrator = models.ForeignKey(Illustrator)
    author = models.ForeignKey(Author)
    synopsis = models.TextField(blank=True)
    def get_absolute_url(self):
      return reverse('btds.views.series',None,[str(self.id)])
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
        return reverse('btds.views.volume',None,[str(self.id)])
    def get_translator(self):
        return sorted(set([x for t in [m.translator.all() for m in self.meta_set.all()] for x in t]))
    def get_editor(self):
        return sorted(set([x for t in [m.editor.all() for m in self.meta_set.all()] for x in t]))
    def get_publisher(self):
        return [m.publisher for m in self.meta_set.all()]
    def get_link(self):
        return list(itertools.chain.from_iterable([m.link_set.all() for m in self.meta_set.all()]))
    def get_cover(self):
        return self.image_set.all()[1:].get().image
    def get_genre(self):
        return self.novel.genre.all()
    def get_link_language(self):
        return sorted(set([x.language for l in [m.link_set.filter(visible = True, closed = False) for m in self.meta_set.all()] for x in l]))
    def __unicode__(self):
        return self.novel.name +' - '+ str(self.number) +' - '+ self.name

class Meta(models.Model):
    volume = models.ForeignKey(Volume)
    language = models.ForeignKey(Language)
    publisher = models.ForeignKey(Publisher, blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)
    chapter_url = models.TextField(blank=True, null=True)
    translator = models.ManyToManyField(Translator, blank=True, null=True)
    editor = models.ManyToManyField(Editor, blank=True, null=True)
    epubgen = models.BooleanField(default=False)
    pdfgen = models.BooleanField(default=False)
    mobigen = models.BooleanField(default=False)
    uuid = models.SlugField(max_length=36, unique=True, default=uuid4())
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.publisher.name + ' - ' + self.volume.novel.name + ' - ' + str(self.volume.number) + ' - ' + self.volume.name

class Link(models.Model):
    meta = models.ForeignKey(Meta)
    language = models.ForeignKey(Language)
    link = models.URLField(max_length=500)
    file_format = models.ForeignKey(Format)
    user = models.ForeignKey(User)
    visible = models.BooleanField(default=False)
    protected = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.link

class Image(models.Model):
    volume = models.ForeignKey(Volume)
    def upload_to_path(instance, filename):
            return 'btds/images/%s/%s' % (instance.volume.id, filename)
    image = models.ImageField(upload_to = upload_to_path)
    cover = models.BooleanField(default=False)
    info = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)