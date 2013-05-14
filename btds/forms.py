#from django import forms
from django.forms import ModelForm
from btds.models import *

class VolumeEditForm(ModelForm):        
    class Meta: 
        model = Volume
        exclude = ('modified','created','novel')
        
class NovelEditForm(ModelForm):        
    class Meta: 
        model = Novel

class AuthorAddForm(ModelForm):        
    class Meta: 
        model = Author

class IllustratorAddForm(ModelForm):        
    class Meta: 
        model = Illustrator

class TranslatorAddForm(ModelForm):        
    class Meta: 
        model = Translator

class EditorAddForm(ModelForm):        
    class Meta: 
        model = Editor

class LanguageAddForm(ModelForm):        
    class Meta: 
        model = Language

class PublisherAddForm(ModelForm):        
    class Meta: 
        model = Publisher

class GenreAddForm(ModelForm):        
    class Meta: 
        model = Genre

class FormatAddForm(ModelForm):        
    class Meta: 
        model = Format

class ImageAddForm(ModelForm):        
    class Meta: 
        model = Image

class NovelAddForm(ModelForm):        
    class Meta: 
        model = Novel

class VolumeAddForm(ModelForm):        
    class Meta: 
        model = Volume
        exclude = ('modified','created')

class MetaAddForm(ModelForm):        
    class Meta: 
        model = Meta
        exclude = ('modified','created','epubgen','pdfgen','mobigen','uuid')

class LinkAddForm(ModelForm):        
    class Meta: 
        model = Link
        exclude = ('modified','created','closed','protected','visible','user','dlcount')