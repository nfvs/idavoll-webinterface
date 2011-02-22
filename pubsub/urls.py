from django.conf.urls.defaults import *

urlpatterns = patterns('pubsub.views',
    (r'^nodes/$', 'nodes_index'),
    (r'^nodes/(?P<node_id>\d+)/$', 'nodes_details'),

    (r'entities/$', 'entities_index'),
    (r'affiliations/$', 'affiliations_index'),
)

