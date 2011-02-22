from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import ObjectDoesNotExist

from pubsub.models import Affiliation

# Create your views here.

from django.http import HttpResponse

def index(request):

	affiliation_list = Affiliation.objects.order_by('entity__jid', 'node__node')
	paginator = Paginator(affiliation_list, 20)

	request_page = request.GET.get('page', '1')
	try:
		page = int(request_page)
	except ValueError:
		if isinstance(request_page, basestring) and request_page == 'last':
			page = paginator.num_pages
		else:
			page = 1

	try:
		affiliations = paginator.page(page)
	except (EmptyPage, InvalidPage):
		affiliations = paginator.page(paginator.num_pages)

	return render_to_response('affiliations/index.html',
							  {'affiliations': affiliations})
