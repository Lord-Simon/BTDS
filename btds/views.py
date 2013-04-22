from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from btds.models import *
from btds.forms import *
from django.conf import settings
from django.template import RequestContext

def index(request):
    if request.user.is_authenticated():
        novels = Novel.objects.all().order_by('name')
        return render_to_response('btdst/index.html', {'novels':novels}, context_instance=RequestContext(request))
    novels = Novel.objects.filter(pk__in=Volume.objects.all().values('novel')).order_by('name')
    return render_to_response('btdst/index.html', {'novels':novels}, context_instance=RequestContext(request))

def series(request, sid):
    novel = get_object_or_404(Novel, id = sid)
    series = novel.volume_set.all().order_by('number', 'id')
    if request.user.is_authenticated():
        nef = NovelEditForm(instance=novel)
        return render_to_response('btdst/series.html',{'series':series, 'NEF':nef, 'NID': sid, 'novel':novel}, context_instance=RequestContext(request))
    return render_to_response('btdst/series.html',{'series':series}, context_instance=RequestContext(request))

def volume(request, vid):
    volume = get_object_or_404(Volume, id = vid)
    if request.user.is_authenticated():
        if volume.meta_set.all():
            d=[]
            [d.append((m.id,MetaAddForm(instance = Meta.objects.get(id = m.id)))) for m in volume.meta_set.all()]
            vef = VolumeEditForm(instance=volume)
            vlaf = LinkAddForm()
            vlaf.fields["meta"].queryset = Meta.objects.filter(volume__id=vid)
            return render_to_response('btdst/volume.html',{'volume':volume, 'VEF':vef, 'MED': dict(d), 'vlaf':vlaf}, context_instance=RequestContext(request))
        vef = VolumeEditForm(instance=volume)
        vlaf = LinkAddForm()
        vlaf.fields["meta"].queryset = Meta.objects.filter(volume__id=vid)
        return render_to_response('btdst/volume.html',{'volume':volume, 'VEF':vef, 'vlaf':vlaf}, context_instance=RequestContext(request))
    return render_to_response('btdst/volume.html',{'volume':volume}, context_instance=RequestContext(request))

def updates(request):
    volumes = Volume.objects.order_by('-id')[:25]
    return render_to_response('btdst/updates.html',{'volumes':volumes}, context_instance=RequestContext(request))
    
def ucp(request):
    if request.user.is_authenticated():
        links = Link.objects.filter(user = request.user, closed = False)
        return render_to_response('btdst/user.html',{'links':links}, context_instance=RequestContext(request))
    return redirect('btds_index')

def ucp_edit_meta(request, lid):
    if request.user.is_authenticated():
        link = Link.objects.get(user = request.user, id=lid, closed = False)
        form = LinkAddForm(instance=link)
        return render_to_response('btdst/user_link_edit.html',{'link':form,'lid':lid}, context_instance=RequestContext(request))
    return redirect('btds_index')

def acp(request):
    if request.user.is_authenticated() and (request.user.groups.filter(name='Admin') or request.user.is_superuser):
        users = User.objects.all()
        d=[]
        [d.append((u.username,{'id':u.id,'links':Link.objects.filter(user=u).count(),'active':Link.objects.filter(user=u,visible=True,closed=False).count(),'pending':Link.objects.filter(user=u,visible=False,closed=False).count(),'protected':Link.objects.filter(user=u,protected=True,visible=True,closed=False).count(),'closed':Link.objects.filter(user=u,closed=True).count()})) for u in User.objects.filter(groups__name='Layer 8', is_active=True)]
        pending = Link.objects.filter(visible=False,closed=False)
        return render_to_response('btdst/admin_users.html',{'users':dict(d),'pl':pending}, context_instance=RequestContext(request))
    return redirect('btds_index')

def acp_pending(request):
    if request.user.is_authenticated() and (request.user.groups.filter(name='Admin') or request.user.is_superuser):
        links = Link.objects.filter(visible=False,closed=False)
        return render_to_response('btdst/acp.html',{'links':links,'acp_pending':'True'}, context_instance=RequestContext(request))
def acp_user_all(request, uid):
    if request.user.is_authenticated() and (request.user.groups.filter(name='Admin') or request.user.is_superuser):
        user = get_object_or_404(User, id = uid, groups__name='Layer 8')
        links = Link.objects.filter(user=user)
        return render_to_response('btdst/acp.html',{'links':links,'acp_user_all':'True'}, context_instance=RequestContext(request))
def acp_user_active(request, uid):
    if request.user.is_authenticated() and (request.user.groups.filter(name='Admin') or request.user.is_superuser):
        user = get_object_or_404(User, id = uid, groups__name='Layer 8')
        links = Link.objects.filter(user=user,visible=True,closed=False)
        return render_to_response('btdst/acp.html',{'links':links,'acp_user_active':'True'}, context_instance=RequestContext(request))
def acp_user_pending(request, uid):
    if request.user.is_authenticated() and (request.user.groups.filter(name='Admin') or request.user.is_superuser):
        user = get_object_or_404(User, id = uid, groups__name='Layer 8')
        links = Link.objects.filter(user=user,visible=False,closed=False)
        return render_to_response('btdst/acp.html',{'links':links,'acp_user_pending':'True'}, context_instance=RequestContext(request))
def acp_user_protected(request, uid):
    if request.user.is_authenticated() and (request.user.groups.filter(name='Admin') or request.user.is_superuser):
        user = get_object_or_404(User, id = uid, groups__name='Layer 8')
        links = Link.objects.filter(user=user,protected=True,closed=False)
        return render_to_response('btdst/acp.html',{'links':links,'acp_user_protected':'True'}, context_instance=RequestContext(request))
def acp_user_closed(request, uid):
    if request.user.is_authenticated() and (request.user.groups.filter(name='Admin') or request.user.is_superuser):
        user = get_object_or_404(User, id = uid, groups__name='Layer 8')
        links = Link.objects.filter(user=user,closed=True)
        return render_to_response('btdst/acp.html',{'links':links,'acp_user_closed':'True'}, context_instance=RequestContext(request))
        

def edit(request):
    if request.user.is_authenticated() and (request.user.groups.filter(name='Admin') or request.user.is_superuser):
        if 'acceptLink' in request.POST:
            link = Link.objects.get(id = request.POST.get("id_link", ""))
            link.visible = True
            link.closed = False
            link.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if request.user.is_authenticated():
        if 'editVolume' in request.POST:
            volume = get_object_or_404(Volume, id = request.POST.get("id_volume", ""))
            form = VolumeEditForm(request.POST or None, instance=volume)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if 'editNovel' in request.POST:
            novel = get_object_or_404(Novel, id = request.POST.get("id_novel", ""))
            form = NovelAddForm(request.POST or None, instance=novel)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if 'editMeta' in request.POST:
            meta = get_object_or_404(Meta, id = request.POST.get("id_meta", ""))
            form = MetaAddForm(request.POST or None, instance=meta)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if 'editLink' in request.POST:
            link = get_object_or_404(Link, user=request.user, id = request.POST.get("id_link", ""))
            form = LinkAddForm(request.POST or None,instance=link)
            if form.is_valid():
                link = form.save(commit=False)
                link.user = request.user
                link.save()
            return redirect('btds_ucp')
    return redirect('btds_index')

def close(request):
    if request.user.is_authenticated():
        if 'closeLink' in request.POST:
            if request.user.groups.filter(name='Admin') or request.user.is_superuser:
                link = Link.objects.get(id = request.POST.get("id_link", ""))
            else:
                link = Link.objects.get(user = request.user, id = request.POST.get("id_link", ""))
            link.closed = True
            link.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if request.user.groups.filter(name='Admin') or request.user.is_superuser:
            if 'closeUser' in request.POST:
                user = User.objects.get(groups__name='Layer 8', id = request.POST.get("id_user", ""))
                for l in Link.objects.filter(user=user):
                    l.closed = True
                    l.save()
                user.is_active = False
                user.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('btds_index')

def add(request):
    if 'addMeta' in request.POST:
        form = MetaAddForm(request.POST or None)
        if form.is_valid():
            form.save()
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
            link = form.save(commit=False)
            link.user = request.user
            link.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))