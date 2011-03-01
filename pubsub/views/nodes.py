from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

from pubsub.models import Node, Affiliation, Subscription


def index(request):

	nodes = Node.objects.all()

	# transform node list in a nested list
	#lists = {}
	#for n in nodes:
	#	b = lists.setdefault(n.node_id, [])
	#	try:
	#	    tmp_id = n.collection.node_id
	#	    lists.setdefault(n.collection.node_id, []).extend([n, b])
		# skip fake root node (collection.node_id=-1, inexisting)
	#	except ObjectDoesNotExist:
	#	    continue

	# remove empty
	#for n in nodes:
	#	if not lists[n.node_id]:
	#		lists[n.collection.node_id].remove(lists[n.node_id])

	return render_to_response('nodes/index.html',
	                          {'nodes': nodes},
	                          context_instance=RequestContext(request))


def details(request, node_id):
    try:
        node = Node.objects.get(pk=node_id)
        affiliations = Affiliation.objects.filter(node=node.node_id)
        num_subscribers = Subscription.objects.filter(node=node.node_id).count()
    except ObjectDoesNotExist:
        node = None
        affiliations = []
        num_subscribers = 0

    return render_to_response('nodes/details.html',
                              {'node': node, 'affiliations': affiliations,
                               'num_subscribers': num_subscribers},
                              context_instance=RequestContext(request))

