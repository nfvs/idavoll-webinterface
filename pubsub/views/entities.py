from django.shortcuts import render_to_response
from django.db.models import Count
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

from pubsub.models import Entity, Subscription, Affiliation

def index(request):

    entities = Entity.objects.annotate(
            subscriptions_count=Count('subscription', distinct=True)).annotate(
            affiliations_count=Count('affiliation', distinct=True)).order_by(
            'jid')

    return render_to_response('entities/index.html',
                              {'entities': entities},
                              context_instance=RequestContext(request))

def details(request, entity_id):

    entity = Entity.objects.select_related().get(pk=entity_id)

    subs_count = Subscription.objects.filter(
            entity__entity_id=entity_id).count()

    affs_count = Affiliation.objects.filter(
            entity__entity_id=entity_id).count()

    return render_to_response('entities/details.html',
            {'entity': entity,
             'subscriptions_count': subs_count,
             'affiliations_count': affs_count})
