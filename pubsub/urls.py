from django.conf.urls.defaults import *

urlpatterns = patterns('pubsub.views',
    # default
    (r'^$', 'generic.index'),

    (r'nodes/$', 'nodes.index'),
    (r'nodes/(?P<node_id>\d+)/$', 'nodes.details'),

    (r'entities/$', 'entities.index'),
    (r'entities/(?P<entity_id>\d+)/$', 'entities.details'),

    (r'affiliations/$', 'affiliations.index'),

    (r'subscriptions/$', 'subscriptions.index'),

    (r'items/$', 'items.index'),
    (r'items/details/(?P<item_id>[\w|\W]+)/$', 'items.details'),
    (r'items/search/$', 'items.search'),
)

