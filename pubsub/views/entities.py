from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

from pubsub.models import Entity, Subscription

def index(request):

    entities = Entity.objects.all()
    return render_to_response('entities/index.html',
                              {'entities': entities},
                              context_instance=RequestContext(request))

def details(request, entity_id):
    
    entity = Entity.objects.get(pk=entity_id)
    
    subscriptions_list = Subscription.objects.filter(entity__entity_id=entity_id)
    
    # paginate subscriptions
    subscriptions = Paginator(subscriptions_list, 20)
    request_page = request.GET.get('page', '1')
    try:
        page = int(request_page)
    except ValueError:
        if isinstance(request_page, basestring) and request_page == 'last':
            page = subscriptions.num_pages
        else:
            page = 1

    try:
        subscriptions = subscriptions.page(page)
    except (EmptyPage, InvalidPage):
        subscriptions = subscriptions.page(subscriptions.num_pages)
    
    return render_to_response('entities/details.html',
                              {'entity': entity,
                               'paginator': subscriptions})