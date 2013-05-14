from django.conf.urls import patterns, include, url
from btds.feeds import VolumeFeed, LinkFeed

urlpatterns = patterns("btds.views",
    url(r'^$', 'index', name="btds_index"),
    url(r'^updates/$', 'updates', name='btds_updates'),
    url(r'^(?P<sid>\d+)/$', 'series', name='btds_series'),
    url(r'^book/(?P<vid>\d+)/$', 'volume', name='btds_volume'),
    url(r'^add/$', 'add', name='btds_add'),
    url(r'^ucp/$', 'ucp', name='btds_ucp'),
    url(r'^ucp/(?P<lid>\d+)/$', 'ucp_edit_meta', name='btds_ucp'),
    url(r'^acp/$', 'acp', name='btds_acp'),
    url(r'^acp/pending/$', 'acp_pending', name='btds_acp_pending'),
    url(r'^acp/(?P<uid>\d+)/all/$', 'acp_user_all', name='btds_acp_user_all'),
    url(r'^acp/(?P<uid>\d+)/active/$', 'acp_user_active', name='btds_acp_user_active'),
    url(r'^acp/(?P<uid>\d+)/pending/$', 'acp_user_pending', name='btds_acp_user_pending'),
    url(r'^acp/(?P<uid>\d+)/protected/$', 'acp_user_protected', name='btds_acp_user_protected'),
    url(r'^acp/(?P<uid>\d+)/closed/$', 'acp_user_closed', name='btds_acp_user_closed'),
    url(r'^close/$', 'close', name='btds_close'),
    url(r'^edit/$', 'edit', name='btds_edit'),
    url(r'^api/$', 'api', name='btds_api'),
)
urlpatterns += patterns("",
    url(r'^login/$','django.contrib.auth.views.login', {'template_name': 'btdst/login.html'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '../'}, name="logout"),
    url(r'^feed/$', VolumeFeed()),
    url(r'^feedl/$', LinkFeed()),
)