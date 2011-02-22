from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import ObjectDoesNotExist

from pubsub.models import Entity

def index(request):

	entities_list = Entity.objects.all()
	paginator = Paginator(entities_list, 20)

	request_page = request.GET.get('page', '1')
	try:
		page = int(request_page)
	except ValueError:
		if isinstance(request_page, basestring) and request_page == 'last':
			page = paginator.num_pages
		else:
			page = 1

	try:
		entities = paginator.page(page)
	except (EmptyPage, InvalidPage):
		entities = paginator.page(paginator.num_pages)

	return render_to_response('entities/index.html',
							  {'entities': entities})

def details(request, entity_id):
    
    entity = Entity.objects.get(pk=entity_id)
    
    return render_to_response('entities/details.html', {'entity': entity})