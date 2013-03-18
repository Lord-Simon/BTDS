from django.conf.urls import patterns, include, url

urlpatterns = patterns("btds",
    url(r'^$', 'views.index', name='index'),
    url(r'^(?P<sid>\d+)/$', 'views.series', name='series'),
    url(r'^\d+/(?P<bid>\d+)/$', 'views.volume', name='volume'),
)
