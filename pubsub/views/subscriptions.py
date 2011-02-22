from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import ObjectDoesNotExist

from pubsub.models import Node, Affiliation, Subscription

def index(request):

	subscriptions_list = Subscription.objects.order_by('entity__jid', 'node__name')
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
							  {'subscriptions': subscriptions})
