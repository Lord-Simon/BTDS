from django.conf.urls import patterns, include, url
from btds.feeds import VolumeFeed, LinkFeed

urlpatterns = patterns("btds.views",
    url(r'^$', 'index', name="btds_index"),
    url(r'^updates/$', 'updates', name='btds_updates'),
    url(r'^(?P<sid>\d+)/$', 'series', name='btds_series'),
    url(r'^book/(?P<vid>\d+)/$', 'volume', name='btds_volume'),
)
urlpatterns += patterns("",
    (r'^feed/$', VolumeFeed()),
    (r'^feedl/$', LinkFeed()),
)