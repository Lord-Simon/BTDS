from django.conf.urls import patterns, include, url
from btds.feeds import VolumeFeed, LinkFeed

urlpatterns = patterns("btds.views",
                       url(r'^$', 'index', name = "btds_index"),
                       url(r'^updates/$', 'updates', name = 'btds_updates'),
                       url(r'^novel/$', 'index', name = 'btds_series_all'),
                       url(r'^novel/(?P<sid>\d+)/$', 'series', name = 'btds_series'),
                       url(r'^book/(?P<vid>\d+)/$', 'volume', name = 'btds_volume'),
                       url(r'^add/$', 'add', name = 'btds_add'),
                       url(r'^ucp/$', 'ucp', name = 'btds_ucp'),
                       url(r'^ucp/(?P<lid>\d+)/$', 'ucp_edit_meta', name = 'btds_ucp_edit_meta'),
                       url(r'^acp/pending/$', 'acp_pending', name = 'btds_acp_pending'),
                       url(r'^acp/$', 'acp', name = 'btds_acp'),
                       url(r'^acp/(?P<uid>\d+)/$', 'acp', name = 'btds_acp_base'),
                       url(r'^acp/(?P<uid>\d+)/all/$', 'acp_user_all', name = 'btds_acp_user_all'),
                       url(r'^acp/(?P<uid>\d+)/active/$', 'acp_user_active', name = 'btds_acp_user_active'),
                       url(r'^acp/(?P<uid>\d+)/pending/$', 'acp_user_pending', name = 'btds_acp_user_pending'),
                       url(r'^acp/(?P<uid>\d+)/protected/$', 'acp_user_protected', name = 'btds_acp_user_protected'),
                       url(r'^acp/(?P<uid>\d+)/closed/$', 'acp_user_closed', name = 'btds_acp_user_closed'),
                       url(r'^close/$', 'close', name = 'btds_close'),
                       url(r'^edit/$', 'edit', name = 'btds_edit'),
                       url(r'^change/(?P<mdl>\w+)$', 'change', name = 'btds_change'),
                       url(r'^change/(?P<mdl>\w+)/(?P<eid>\d+)/$', 'change_entry', name = 'btds_change_entry'),
)

urlpatterns += patterns("",
                        url(r'^feed/$', VolumeFeed(), name = 'btds_feed'),
                        url(r'^feedl/$', LinkFeed(), name = 'btds_feed_links'),
)
urlpatterns += patterns('django.contrib.flatpages.views',
                        url(r'^about/$', 'flatpage', {'url':'/about/'}, name = 'btds_about'),
                        url(r'^disclaimer/$', 'flatpage', {'url':'/disclaimer/'}, name = 'btds_disclaimer'),
)