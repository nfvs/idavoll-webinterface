from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

from pubsub.models import Affiliation, Entity, Node

# Create your views here.

from django.http import HttpResponse

def index(request):

    affiliations = Affiliation.objects.order_by('entity__jid', 'node__name')
    
    # filters
    try:
        filters = {}
        request_entity = request.GET.get('entity', None)
        request_node = request.GET.get('node', None)
        if request_entity:
            affiliations = affiliations.filter(entity__entity_id=request_entity)
            filters['Entity'] = Entity.objects.get(pk=request_entity).jid
        if request_node:
            affiliations = affiliations.filter(node__node_id=request_node)
            filters['Node'] = Node.objects.get(pk=request_node).name
    except ObjectDoesNotExist:
        pass

    return render_to_response('affiliations/index.html',
                              {'affiliations': affiliations,
                               'filters': filters},
                               context_instance=RequestContext(request))
