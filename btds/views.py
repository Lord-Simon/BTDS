from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from uuid import uuid4
from django.core import serializers
from btds.models import *
from btds.forms import *
from django.template import RequestContext


def api(request):
    return HttpResponse(serializers.serialize("json", Novel.objects.all()))


def index(request):
    if request.user.is_authenticated():
        novels = Novel.objects.all().order_by('name')
        return render_to_response('btds/index.html', {'novels':novels}, context_instance = RequestContext(request))
    novels = Novel.objects.filter(pk__in = Volume.objects.all().values('novel')).order_by('name')
    return render_to_response('btds/index.html', {'novels':novels}, context_instance = RequestContext(request))


def series(request, sid):
    novel = get_object_or_404(Novel, id = sid)
    if request.user.is_authenticated():
        series = novel.volume_set.all().order_by('number', 'id')
        nef = NovelEditForm(instance = novel)
        return render_to_response('btds/series.html', {'series':series, 'NEF':nef, 'NID':sid, 'novel':novel},
                                  context_instance = RequestContext(request))
    series = novel.volume_set.filter(pk__in = Meta.objects.all().values('volume')).order_by('number', 'id')
    return render_to_response('btds/series.html', {'series':series}, context_instance = RequestContext(request))


def volume(request, vid):
    volume = get_object_or_404(Volume, id = vid)
    vef = VolumeEditForm(instance = volume)
    vlaf = LinkAddForm()
    viaf = ImageAddForm()
    vlaf.fields["meta"].queryset = Meta.objects.filter(volume__id = vid)
    viaf.fields["meta"].queryset = Meta.objects.filter(volume__id = vid)
    if request.user.is_authenticated():
        if volume.meta_set.all():
            d = []
            [d.append((m.id, MetaAddForm(instance = Meta.objects.get(id = m.id)))) for m in volume.meta_set.all()]
            return render_to_response('btds/volume.html',
                                      {'volume':volume, 'VEF':vef, 'MED':dict(d), 'vlaf':vlaf, 'viaf':viaf},
                                      context_instance = RequestContext(request))
        return render_to_response('btds/volume.html', {'volume':volume, 'VEF':vef, 'vlaf':vlaf, 'viaf':viaf},
                                  context_instance = RequestContext(request))
    return render_to_response('btds/volume.html', {'volume':volume}, context_instance = RequestContext(request))


def updates(request):
    volumes = Volume.objects.order_by('-id')[:25]
    return render_to_response('btds/updates.html', {'volumes':volumes}, context_instance = RequestContext(request))


@login_required(login_url = '/accounts/login/')
def ucp(request):
    if request.user.is_authenticated():
        links = Link.objects.filter(user = request.user, closed = False)
        return render_to_response('btds/user.html', {'links':links}, context_instance = RequestContext(request))
    return redirect('btds_index')


@login_required(login_url = '/accounts/login/')
def ucp_edit_meta(request, lid):
    if request.user.is_authenticated():
        link = Link.objects.get(user = request.user, id = lid, closed = False)
        form = LinkAddForm(instance = link)
        return render_to_response('btds/user_link_edit.html', {'link':form, 'lid':lid},
                                  context_instance = RequestContext(request))
    return redirect('btds_index')


@login_required(login_url = '/accounts/login/')
def acp(request):
    if request.user.is_authenticated() and (request.user.groups.filter(name = 'Admin') or request.user.is_superuser):
        d = []
        [d.append((u.username, {'id':u.id, 'links':Link.objects.filter(user = u).count(),
                                'active':Link.objects.filter(user = u, visible = True, closed = False).count(),
                                'pending':Link.objects.filter(user = u, visible = False, closed = False).count(),
                                'protected':Link.objects.filter(user = u, protected = True, visible = True,
                                                                closed = False).count(),
                                'closed':Link.objects.filter(user = u, closed = True).count()})) for u in
         User.objects.filter(groups__name = 'Layer 8', is_active = True)]
        pending = Link.objects.filter(visible = False, closed = False)
        return render_to_response('btds/admin_users.html', {'users':dict(d), 'pl':pending},
                                  context_instance = RequestContext(request))
    return redirect('btds_index')


@login_required(login_url = '/accounts/login/')
def acp_pending(request):
    if request.user.is_authenticated() and (request.user.groups.filter(name = 'Admin') or request.user.is_superuser):
        links = Link.objects.filter(visible = False, closed = False)
        return render_to_response('btds/acp.html', {'links':links, 'acp_pending':'True'},
                                  context_instance = RequestContext(request))


@login_required(login_url = '/accounts/login/')
def acp_user_all(request, uid):
    if request.user.is_authenticated() and (request.user.groups.filter(name = 'Admin') or request.user.is_superuser):
        user = get_object_or_404(User, id = uid, groups__name = 'Layer 8')
        links = Link.objects.filter(user = user)
        return render_to_response('btds/acp.html', {'links':links, 'acp_user_all':'True'},
                                  context_instance = RequestContext(request))


@login_required(login_url = '/accounts/login/')
def acp_user_active(request, uid):
    if request.user.is_authenticated() and (request.user.groups.filter(name = 'Admin') or request.user.is_superuser):
        user = get_object_or_404(User, id = uid, groups__name = 'Layer 8')
        links = Link.objects.filter(user = user, visible = True, closed = False)
        return render_to_response('btds/acp.html', {'links':links, 'acp_user_active':'True'},
                                  context_instance = RequestContext(request))


@login_required(login_url = '/accounts/login/')
def acp_user_pending(request, uid):
    if request.user.is_authenticated() and (request.user.groups.filter(name = 'Admin') or request.user.is_superuser):
        user = get_object_or_404(User, id = uid, groups__name = 'Layer 8')
        links = Link.objects.filter(user = user, visible = False, closed = False)
        return render_to_response('btds/acp.html', {'links':links, 'acp_user_pending':'True'},
                                  context_instance = RequestContext(request))


@login_required(login_url = '/accounts/login/')
def acp_user_protected(request, uid):
    if request.user.is_authenticated() and (request.user.groups.filter(name = 'Admin') or request.user.is_superuser):
        user = get_object_or_404(User, id = uid, groups__name = 'Layer 8')
        links = Link.objects.filter(user = user, protected = True, closed = False)
        return render_to_response('btds/acp.html', {'links':links, 'acp_user_protected':'True'},
                                  context_instance = RequestContext(request))


@login_required(login_url = '/accounts/login/')
def acp_user_closed(request, uid):
    if request.user.is_authenticated() and (request.user.groups.filter(name = 'Admin') or request.user.is_superuser):
        user = get_object_or_404(User, id = uid, groups__name = 'Layer 8')
        links = Link.objects.filter(user = user, closed = True)
        return render_to_response('btds/acp.html', {'links':links, 'acp_user_closed':'True'},
                                  context_instance = RequestContext(request))


@login_required(login_url = '/accounts/login/')
def edit(request):
    if 'linkDownloadCount' in request.POST:
        link = get_object_or_404(Link, closed = False, id = request.POST.get("id_link", ""))
        link.incr_dlcount()
        return HttpResponse()
    if request.user.is_authenticated() and (request.user.groups.filter(name = 'Admin') or request.user.is_superuser):
        if 'acceptLink' in request.POST:
            link = Link.objects.get(id = request.POST.get("id_link", ""))
            link.visible = True
            link.closed = False
            link.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if request.user.is_authenticated():
        if 'editAuthor' in request.POST:
            change = get_object_or_404(Author, id = request.POST.get("id_author", ""))
            form = AuthorAddForm(request.POST or None, instance = change)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.REQUEST.get('next'))
        if 'editIllustrator' in request.POST:
            change = get_object_or_404(Illustrator, id = request.POST.get("id_illustrator", ""))
            form = IllustratorAddForm(request.POST or None, instance = change)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.REQUEST.get('next'))
        if 'editTranslator' in request.POST:
            change = get_object_or_404(Translator, id = request.POST.get("id_translator", ""))
            form = TranslatorAddForm(request.POST or None, instance = change)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.REQUEST.get('next'))
        if 'editEditor' in request.POST:
            change = get_object_or_404(Editor, id = request.POST.get("id_editor", ""))
            form = EditorAddForm(request.POST or None, instance = change)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.REQUEST.get('next'))
        if 'editLanguage' in request.POST:
            change = get_object_or_404(Language, id = request.POST.get("id_language", ""))
            form = LanguageAddForm(request.POST or None, instance = change)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.REQUEST.get('next'))
        if 'editPublisher' in request.POST:
            change = get_object_or_404(Publisher, id = request.POST.get("id_publisher", ""))
            form = PublisherAddForm(request.POST or None, instance = change)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.REQUEST.get('next'))
        if 'editImage' in request.POST:
            change = get_object_or_404(Image, id = request.POST.get("id_image", ""))
            form = ImageEditForm(request.POST or None, instance = change)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.REQUEST.get('next'))
        if 'editVolume' in request.POST:
            volume = get_object_or_404(Volume, id = request.POST.get("id_volume", ""))
            form = VolumeEditForm(request.POST or None, instance = volume)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if 'editNovel' in request.POST:
            novel = get_object_or_404(Novel, id = request.POST.get("id_novel", ""))
            form = NovelAddForm(request.POST or None, instance = novel)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if 'editMeta' in request.POST:
            meta = get_object_or_404(Meta, id = request.POST.get("id_meta", ""))
            form = MetaAddForm(request.POST or None, instance = meta)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if 'editLink' in request.POST:
            link = get_object_or_404(Link, user = request.user, id = request.POST.get("id_link", ""))
            form = LinkAddForm(request.POST or None, instance = link)
            if form.is_valid():
                link = form.save(commit = False)
                link.user = request.user
                link.save()
            return redirect('btds_ucp')
        if 'makeCover' in request.POST:
            image = get_object_or_404(Image, id = request.POST.get("id_image", ""))
            vol = get_object_or_404(Volume, id = request.POST.get("id_volume", ""))
            Image.objects.filter(volume = vol).update(cover = False)
            image.cover = True
            image.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('btds_index')


@login_required(login_url = '/accounts/login/')
def close(request):
    if request.user.is_authenticated():
        if 'closeLink' in request.POST:
            if request.user.groups.filter(name = 'Admin') or request.user.is_superuser:
                link = Link.objects.get(id = request.POST.get("id_link", ""))
            else:
                link = Link.objects.get(user = request.user, id = request.POST.get("id_link", ""))
            link.closed = True
            link.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if request.user.groups.filter(name = 'Admin') or request.user.is_superuser:
            if 'closeUser' in request.POST:
                user = User.objects.get(groups__name = 'Layer 8', id = request.POST.get("id_user", ""))
                for l in Link.objects.filter(user = user):
                    l.closed = True
                    l.save()
                user.is_active = False
                user.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if request.user.is_authenticated():
            if 'deleteImage' in request.POST:
                image = get_object_or_404(Image, id = request.POST.get("id_image", ""))
                image.delete()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('btds_index')


@login_required(login_url = '/accounts/login/')
def add(request):
    if 'addMeta' in request.POST:
        form = MetaAddForm(request.POST or None)
        if form.is_valid():
            meta = form.save(commit = False)
            meta.uuid = uuid4()
            meta.save()
    if 'addAuthor' in request.POST:
        form = AuthorAddForm(request.POST or None)
        if form.is_valid():
            form.save()
    if 'addIllustrator' in request.POST:
        form = IllustratorAddForm(request.POST or None)
        if form.is_valid():
            form.save()
    if 'addTranslator' in request.POST:
        form = TranslatorAddForm(request.POST or None)
        if form.is_valid():
            form.save()
    if 'addEditor' in request.POST:
        form = EditorAddForm(request.POST or None)
        if form.is_valid():
            form.save()
    if 'addLanguage' in request.POST:
        form = LanguageAddForm(request.POST or None)
        if form.is_valid():
            form.save()
    if 'addPublisher' in request.POST:
        form = PublisherAddForm(request.POST or None)
        if form.is_valid():
            form.save()
    if 'addGenre' in request.POST:
        form = GenreAddForm(request.POST or None)
        if form.is_valid():
            form.save()
    if 'addFormat' in request.POST:
        form = FormatAddForm(request.POST or None)
        if form.is_valid():
            form.save()
    if 'addImage' in request.POST:
        form = ImageAddForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
    if 'addNovel' in request.POST:
        form = NovelAddForm(request.POST or None)
        if form.is_valid():
            form.save()
    if 'addVolume' in request.POST:
        form = VolumeAddForm(request.POST or None)
        if form.is_valid():
            form.save()
    if 'addLink' in request.POST:
        form = LinkAddForm(request.POST or None)
        if form.is_valid():
            link = form.save(commit = False)
            link.user = request.user
            link.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url = '/accounts/login/')
def change(request, mdl):
    if 'author' in mdl:
        change = Author.objects.all()
        return render_to_response('btds/change.html', {'change_list':change, 'edit':'author'},
                                  context_instance = RequestContext(request))
    elif 'illustrator' in mdl:
        change = Illustrator.objects.all()
        return render_to_response('btds/change.html', {'change_list':change, 'edit':'illustrator'},
                                  context_instance = RequestContext(request))
    elif 'translator' in mdl:
        change = Translator.objects.all()
        return render_to_response('btds/change.html', {'change_list':change, 'edit':'translator'},
                                  context_instance = RequestContext(request))
    elif 'editor' in mdl:
        change = Editor.objects.all()
        return render_to_response('btds/change.html', {'change_list':change, 'edit':'editor'},
                                  context_instance = RequestContext(request))
    elif 'language' in mdl:
        change = Language.objects.all()
        return render_to_response('btds/change.html', {'change_list':change, 'edit':'language'},
                                  context_instance = RequestContext(request))
    elif 'publisher' in mdl:
        change = Publisher.objects.all()
        return render_to_response('btds/change.html', {'change_list':change, 'edit':'publisher'},
                                  context_instance = RequestContext(request))
    elif 'image' in mdl:
        change = Image.objects.all()
        return render_to_response('btds/change.html', {'change_list':change, 'edit':'image'},
                                  context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url = '/accounts/login/')
def change_entry(request, mdl, eid):
    if 'author' in mdl:
        change = get_object_or_404(Author, id = eid)
        form = AuthorAddForm(instance = change)
        return render_to_response('btds/change_entry.html', {'form':form, 'edit':'author', 'eid':eid},
                                  context_instance = RequestContext(request))
    elif 'illustrator' in mdl:
        change = get_object_or_404(Illustrator, id = eid)
        form = IllustratorAddForm(instance = change)
        return render_to_response('btds/change_entry.html', {'form':form, 'edit':'illustrator', 'eid':eid},
                                  context_instance = RequestContext(request))
    elif 'translator' in mdl:
        change = get_object_or_404(Translator, id = eid)
        form = TranslatorAddForm(instance = change)
        return render_to_response('btds/change_entry.html', {'form':form, 'edit':'translator', 'eid':eid},
                                  context_instance = RequestContext(request))
    elif 'editor' in mdl:
        change = get_object_or_404(Editor, id = eid)
        form = EditorAddForm(instance = change)
        return render_to_response('btds/change_entry.html', {'form':form, 'edit':'editor', 'eid':eid},
                                  context_instance = RequestContext(request))
    elif 'language' in mdl:
        change = get_object_or_404(Language, id = eid)
        form = LanguageAddForm(instance = change)
        return render_to_response('btds/change_entry.html', {'form':form, 'edit':'language', 'eid':eid},
                                  context_instance = RequestContext(request))
    elif 'publisher' in mdl:
        change = get_object_or_404(Publisher, id = eid)
        form = PublisherAddForm(instance = change)
        return render_to_response('btds/change_entry.html', {'form':form, 'edit':'publisher', 'eid':eid},
                                  context_instance = RequestContext(request))
    elif 'image' in mdl:
        change = get_object_or_404(Image, id = eid)
        form = ImageEditForm(instance = change)
        form.fields["meta"].queryset = Meta.objects.filter(volume__id = change.volume.id)
        return render_to_response('btds/change_entry.html', {'form':form, 'edit':'image', 'eid':eid, 'img':change},
                                  context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))