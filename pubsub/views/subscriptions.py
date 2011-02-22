from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

from pubsub.models import Node, Affiliation, Subscription, Entity

def index(request):
    
    subscriptions = Subscription.objects.order_by('entity__jid', 'node__name')
    
    # filters
    try:
        filters = {}
        request_entity = request.GET.get('entity', None)
        request_node = request.GET.get('node', None)
        if request_entity:
            subscriptions = subscriptions.filter(entity__entity_id=request_entity)
            filters['Entity'] = Entity.objects.get(pk=request_entity).jid
        if request_node:
            subscriptions = subscriptions.filter(node__node_id=request_node)
            filters['Node'] = Node.objects.get(pk=request_node).name
    except ObjectDoesNotExist:
        pass

    return render_to_response('subscriptions/index.html',
                              {'subscriptions': subscriptions,
                               'filters': filters},
                                  context_instance=RequestContext(request))
