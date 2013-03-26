from django.conf.urls import patterns, include, url
from btds.feeds import VolumeFeed, LinkFeed

urlpatterns = patterns("btds.views",
    url(r'^$', 'index', name="btds_index"),
    url(r'^updates/$', 'updates', name='btds_updates'),
    url(r'^(?P<sid>\d+)/$', 'series', name='btds_series'),
    url(r'^book/(?P<vid>\d+)/$', 'volume', name='btds_volume'),
)
urlpatterns += patterns("",
    url(r'^login/$','django.contrib.auth.views.login', {'template_name': 'btdst/login.html'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '../'}, name="logout"),
    url(r'^feed/$', VolumeFeed()),
    url(r'^feedl/$', LinkFeed()),
)