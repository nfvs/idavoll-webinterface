from django.shortcuts import render_to_response
from django.template import RequestContext

from couchdbkit.ext.django.loading import get_db

from pubsub.models import Node, Entity, Affiliation, Subscription, Item

def index(request):
    try:
        info = get_db('pubsub').info()
        num_items = info[u'doc_count']
    except:
        num_items = ''
        
    num_nodes = Node.objects.all().count()
    num_entities = Entity.objects.all().count()
    num_subscriptions = Subscription.objects.all().count()
    num_affiliations = Affiliation.objects.all().count()
    return render_to_response('index.html',
                              {'num_nodes': num_nodes,
                               'num_items': num_items,
                               'num_entities': num_entities,
                               'num_subscriptions': num_subscriptions,
                               'num_affiliations': num_affiliations},
                              context_instance=RequestContext(request))