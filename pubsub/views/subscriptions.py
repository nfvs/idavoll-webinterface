from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import ObjectDoesNotExist

from pubsub.models import Node, Affiliation, Subscription, Entity

def index(request):
    
    subscriptions_list = Subscription.objects.order_by('entity__jid', 'node__name')
    
    # filters
    try:
        filters = {}
        request_entity = request.GET.get('entity', None)
        request_node = request.GET.get('node', None)
        if request_entity:
            subscriptions_list = subscriptions_list.filter(entity__entity_id=request_entity)
            filters['Entity'] = Entity.objects.get(pk=request_entity).jid
        if request_node:
            subscriptions_list = subscriptions_list.filter(node__node_id=request_node)
            filters['Node'] = Node.objects.get(pk=request_node).name
    except ObjectDoesNotExist:
        pass
        
    paginator = Paginator(subscriptions_list, 20)

    request_page = request.GET.get('page', '1')
    
    try:
        page = int(request_page)
    except ValueError:
        if isinstance(request_page, basestring) and request_page == 'last':
            page = paginator.num_pages
        else:
            page = 1

    try:
        subscriptions = paginator.page(page)
    except (EmptyPage, InvalidPage):
        subscriptions = paginator.page(paginator.num_pages)

    return render_to_response('subscriptions/index.html',
                              {'paginator': subscriptions,
                               'filters': filters})
