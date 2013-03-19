from django.conf.urls import patterns, include, url

urlpatterns = patterns("btds.views",
    url(r'^$', 'index', name='index'),
    url(r'^(?P<sid>\d+)/$', 'series', name='series'),
    url(r'^(?P<vid>\d+)/$', 'volume', name='volume'),
)
