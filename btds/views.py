from django.shortcuts import render_to_response, get_object_or_404
from btds.models import *
from django.conf import settings

def index(request):
    
    return render_to_response('btegen/index.html')

def series(request, sid):
    novel = get_object_or_404(Novel, id = sid)
    return render_to_response('btegen/series.html',{'series':novel})

def book(request, bid):
    volume = get_object_or_404(Volume, id = bid)
    return render_to_response('btegen/book.html',{'book':volume})
