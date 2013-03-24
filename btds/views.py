from django.shortcuts import render_to_response, get_object_or_404
from btds.models import *
from django.conf import settings

def index(request):
    novels = Novel.objects.all()
    return render_to_response('btdst/index.html',{'novels':novels})

def series(request, sid):
    novel = get_object_or_404(Novel, id = sid)
    series = novel.volume_set.all()
    return render_to_response('btdst/series.html',{'series':series})

def volume(request, vid):
    volume = get_object_or_404(Volume, id = vid)
    return render_to_response('btdst/volume.html',{'volume':volume})

def updates(request):
    volumes = Volume.objects.order_by('-id')[:25]
    return render_to_response('btdst/updates.html',{'volumes':volumes})