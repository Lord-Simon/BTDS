from django.contrib.syndication.views import Feed
from django.utils import feedgenerator
from btds.models import Volume, Link


class VolumeFeed(Feed):
    feed_type = feedgenerator.Rss201rev2Feed
    title = "Baka Tsuki Destribution System"
    link = "/"
    description = "Updates on added Novels"

    def items(self):
        return Volume.objects.order_by('-id')[:25]

    def item_title(self, item):
        return item.novel.name + " - " + str(item.number) + " - " + item.name

    def item_categories(self, item):
        return item.novel.genre.all()

    def item_pubdate(self, item):
        return item.created

    def item_description(self, item):
        return item.synopsis

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return item.get_absolute_url()


class AtomVolumeFeed(VolumeFeed):
    feed_type = feedgenerator.Atom1Feed


class LinkFeed(Feed):
    title = "Baka Tsuki Destribution System"
    link = "/"
    description = "Links published on BTDS"

    def items(self):
        return Link.objects.filter(visible = True, closed = False).order_by('-id')[:25]

    def item_title(self, item):
        return item.meta.volume.novel.name + " - " + str(item.meta.volume.number) + " - " + item.meta.volume.name

    def item_description(self, item):
        return "<a href=" + str(item.link) + ">" + str(item.file_format) + " by " + str(item.user) + "</a>"

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return item.meta.volume.get_absolute_url()