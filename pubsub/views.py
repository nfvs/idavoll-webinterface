from collections import defaultdict

from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from pubsub.models import *

# Create your views here.

from django.http import HttpResponse


def nodes_index(request):

    nodes = Node.objects.all()

    # transform node list in a nested list
    lists = {}
    for n in nodes:
        b = lists.setdefault(n.node_id, [])
        lists.setdefault(n.collection, []).extend([n.node, b])

    # remove empty
    for n in nodes:
        if not lists[n.node_id]:
            lists[n.collection].remove(lists[n.node_id])

    import itertools
    print list(itertools.chain(*lists))

    return render_to_response('nodes/index.html', {'nodes': lists[0]})


def affiliations_index(request):

    affiliation_list = Affiliation.objects.order_by('entity__jid', 'node__node')
    paginator = Paginator(affiliation_list, 20)

    request_page = request.GET.get('page', '1')
    try:
        page = int(request_page)
    except ValueError:
        if request_page == 'last':
            page = paginator.num_pages
        else:
            page = 1

    try:
        affiliations = paginator.page(page)
    except (EmptyPage, InvalidPage):
        affiliations = paginator.page(paginator.num_pages)

    return render_to_response('affiliations/index.html',
                              {'affiliations': affiliations})
