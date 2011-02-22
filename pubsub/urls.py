from django.conf.urls.defaults import *

urlpatterns = patterns('pubsub.views',
    # default
    (r'^$', 'entities.index'),

    (r'nodes/$', 'nodes.index'),
    (r'nodes/(?P<node_id>\d+)/$', 'nodes.details'),

    (r'entities/$', 'entities.index'),
    (r'entities/(?P<entity_id>\d+)/$', 'entities.details'),
    
    (r'affiliations/$', 'affiliations.index'),
    
    (r'subscriptions/$', 'subscriptions.index'),
)

