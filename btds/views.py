from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from btds.models import *
from btds.forms import *
from django.conf import settings
from django.template import RequestContext

def index(request):
    novels = Novel.objects.all()
    return render_to_response('btdst/index.html', {'novels':novels}, context_instance=RequestContext(request))

def series(request, sid):
    novel = get_object_or_404(Novel, id = sid)
    series = novel.volume_set.all()
    return render_to_response('btdst/series.html',{'series':series}, context_instance=RequestContext(request))

def volume(request, vid):
    volume = get_object_or_404(Volume, id = vid)
    return render_to_response('btdst/volume.html',{'volume':volume}, context_instance=RequestContext(request))

def updates(request):
    volumes = Volume.objects.order_by('-id')[:25]
    return render_to_response('btdst/updates.html',{'volumes':volumes}, context_instance=RequestContext(request))

def selectedit(request, vid):
    volume = get_object_or_404(Volume, id = vid)
    vef = VolumeEditForm(instance=volume)
    metas = volume.meta_set.all()
    return render_to_response('btdst/select_edit.html',{'metas':metas, 'VEF':vef}, context_instance=RequestContext(request))

def editmeta(request, vid, pid):
    meta = get_object_or_404(Meta, volume = vid, publisher=pid)
    return render_to_response('btdst/edit_meta.html',{'meta':meta}, context_instance=RequestContext(request))
    
def ucp(request):
    if request.user.is_authenticated():
        links = Link.objects.filter(user = request.user, closed = False)
        return render_to_response('btdst/user.html',{'links':links}, context_instance=RequestContext(request))
    return redirect('btds_index')
    
def close(request):
    if request.user.is_authenticated():
        if 'closeLink' in request.POST:
            link = Link.objects.get(user = request.user, id = request.POST.get("id_link", ""))
            link.closed = True
            link.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('btds_index')

def add(request):
    if 'addMeta' in request.POST:
        form = MetaAddForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'addAuthor' in request.POST:
        form = AuthorAddForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'addIllustrator' in request.POST:
        form = IllustratorAddForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'addTranslator' in request.POST:
        form = TranslatorAddForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'addEditor' in request.POST:
        form = EditorAddForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'addLanguage' in request.POST:
        form = LanguageAddForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'addPublisher' in request.POST:
        form = PublisherAddForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'addGenre' in request.POST:
        form = GenreAddForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'addFormat' in request.POST:
        form = FormatAddForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'addImage' in request.POST:
        form = ImageAddForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'addNovel' in request.POST:
        form = NovelAddForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'addVolume' in request.POST:
        form = VolumeAddForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'addLink' in request.POST:
        form = LinkAddForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))