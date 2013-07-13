from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from uuid import uuid4
import itertools, string

PUBLISHER_TYPE = (
    ('m', 'MediaWiki'),
    ('w', 'WordPress'),
    ('b', 'BlogSpot'),
)


class Author(models.Model):
    name = models.CharField(max_length = 255, unique = True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Illustrator(models.Model):
    name = models.CharField(max_length = 255, unique = True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Translator(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    link = models.URLField(max_length = 500, blank = True, null = True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Editor(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    link = models.URLField(max_length = 500, blank = True, null = True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Language(models.Model):
    name = models.CharField(max_length = 255)
    iso = models.SlugField(max_length = 2, unique = True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Publisher(models.Model):
    name = models.CharField(max_length = 255)
    publisher_type = models.CharField(max_length = 1, choices = PUBLISHER_TYPE)
    link = models.URLField(max_length = 500, blank = True, null = True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Genre(models.Model):
    name = models.CharField(max_length = 255, unique = True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Format(models.Model):
    name = models.CharField(max_length = 5, unique = True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Novel(models.Model):
    name = models.CharField(max_length = 255, blank = False)
    genre = models.ManyToManyField(Genre, blank = True, null = True)
    illustrator = models.ForeignKey(Illustrator, blank = True, null = True)
    author = models.ForeignKey(Author)
    synopsis = models.TextField(blank = True)

    def get_absolute_url(self):
        return reverse('btds.views.series', None, [str(self.id)])

    def __unicode__(self):
        return self.name


class Volume(models.Model):
    name = models.CharField(max_length = 255, blank = True)
    number = models.DecimalField(blank = True, null = True, decimal_places=1, max_digits=10)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)
    novel = models.ForeignKey(Novel, related_name="volume")
    synopsis = models.TextField(blank = True)
    isbn = models.CharField(max_length = 17, blank = True)
    year = models.PositiveSmallIntegerField(max_length = 4, blank = True, null = True)

    def get_absolute_url(self):
        return reverse('btds.views.volume', None, [str(self.id)])

    def get_translator(self):
        return sorted(set([x for t in [m.translator.all() for m in self.meta.all()] for x in t]))

    def get_editor(self):
        return sorted(set([x for t in [m.editor.all() for m in self.meta.all()] for x in t]))

    def get_publisher(self):
        return [m.publisher for m in self.meta.all()]

    def get_link(self):
        return list(itertools.chain.from_iterable([m.link.all() for m in self.meta.all()]))

    def get_link_visible(self):
        return list(itertools.chain.from_iterable([m.link.filter(visible=True, closed=False) for m in self.meta.all()]))

    def get_links_pending(self):
        return list(itertools.chain.from_iterable([m.link.filter(visible=False, closed=False) for m in self.meta.all()]))

    def get_cover(self):
        return self.image_set.filter(cover = True)[:1].get().image

    def get_images(self):
        return self.image_set.all().order_by('cover', 'image')

    def get_genre(self):
        return self.novel.genre.all()

    def get_link_language(self):
        return sorted(set([x.language for l in [m.link.filter(visible = True, closed = False) for m in self.meta.all()] for x in l]))

    def __unicode__(self):
        volume_name = self.novel.name
        if self.number:
            volume_name += ' - Volume ' + str(self.number)
        if self.name:
            volume_name += ' - ' + self.name
        return volume_name


class Meta(models.Model):
    volume = models.ForeignKey(Volume, related_name="meta")
    language = models.ForeignKey(Language, related_name="meta")
    publisher = models.ForeignKey(Publisher, related_name="meta")
    url = models.URLField(max_length = 500, blank = True, null = True)
    chapter_url = models.TextField(blank = True, null = True)
    translator = models.ManyToManyField(Translator, blank = True, null = True, related_name="meta")
    editor = models.ManyToManyField(Editor, blank = True, null = True, related_name="meta")
    epubgen = models.BooleanField(default = False)
    pdfgen = models.BooleanField(default = False)
    mobigen = models.BooleanField(default = False)
    def generateUUID():
        return str(uuid4())
    uuid = models.SlugField(max_length = 36, unique = True, editable=False, default=generateUUID())
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.uuid = uuid4()
            super(Meta, self).save(*args, **kwargs)
        super(Meta, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.publisher.name + ' - ' + self.volume.novel.name + ' - ' + str(
            self.volume.number) + ' - ' + self.volume.name


class Link(models.Model):
    meta = models.ForeignKey(Meta, related_name="link")
    language = models.ForeignKey(Language, related_name="link")
    link = models.URLField(max_length = 500)
    file_format = models.ForeignKey(Format, related_name="link")
    user = models.ForeignKey(User)
    dlcount = models.BigIntegerField(default = 0)
    visible = models.BooleanField(default = False)
    protected = models.BooleanField(default = False)
    closed = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def get_absolute_url(self):
        return reverse('btds.views.ucp_edit_meta', None, [str(self.id)])

    def __unicode__(self):
        return self.link


class Image(models.Model):
    name = models.CharField(max_length = 255, blank = True, null = True)
    volume = models.ForeignKey(Volume)

    def upload_to_path(instance, filename):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = ''.join(c for c in filename if c in valid_chars)
        return 'btds/images/%s/%s' % (instance.volume.id, filename)

    image = models.ImageField(upload_to = upload_to_path)
    cover = models.BooleanField(default = False)
    meta = models.ManyToManyField(Meta, blank = True, null = True)
    info = models.TextField(blank = True)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs):
        if not self.name:
            super(Image, self).save(*args, **kwargs)
            self.name = str(self.image).split("/")[-1]
        super(Image, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.image).split("/")[-1]