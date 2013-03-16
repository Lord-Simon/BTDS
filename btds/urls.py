from django.conf.urls import patterns, include, url

urlpatterns = patterns("",
    url(r'^$', 'btds.views.index', name='index'),
    url(r'^(?P<sid>\d+)/$', 'btds.views.series', name='series'),
    url(r'^\d+/(?P<bid>\d+)/$', 'btds.views.book', name='book'),
)