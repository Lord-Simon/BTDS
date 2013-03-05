from django.shortcuts import render_to_response, get_object_or_404
from btds.models import *
from django.conf import settings

def index(request):
    
    return render_to_response('btegen/index.html',{})

def series(request, sid):
    return render_to_response('btegen/series.html',{})

def book(request, bid):
    return render_to_response('btegen/book.html',{})
