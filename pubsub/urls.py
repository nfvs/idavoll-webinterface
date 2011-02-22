from django.conf.urls.defaults import *

urlpatterns = patterns('pubsub.views',
    (r'^nodes/$', 'nodes_index'),

    (r'entities/$', 'entities_index'),
    (r'affiliations/$', 'affiliations_index'),
)

