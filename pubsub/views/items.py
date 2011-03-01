import types
import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers


from couchdbkit.ext.django.loading import get_db
from couchdbkit import ResourceNotFound
from couchdbkit.ext.django.schema import *

from pubsub.models import Item, Node


def convert_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % bytes
    return size

def index(request):

    info = get_db('pubsub').info()
    info['disk_size'] = convert_bytes(info['disk_size'])

    node_id = request.GET.get('node')
    if node_id:
        try:
            node = Node.objects.get(pk=node_id)
        except ObjectDoesNotExist:
            return render_to_response('items/list.html',
                                      {'error': 'node_not_found'},
                                      context_instance=RequestContext(request))

        node_type = node.node_type
        node_name = node.name

        if node_type == 'collection':
            return render_to_response('items/list.html',
                                      {'error': 'collection',
                                       'node_name': node_name},
                                      context_instance=RequestContext(request))

        items = Item.view('pubsub/items_by_node_date',
                          startkey=[node_name, {}],
                          endkey=[node_name],
                          descending=True,
                          limit=20,
                          include_docs=True)
        return render_to_response('items/list.html',
                                  {'items': items,
                                   'node_name': node_name},
                                  context_instance=RequestContext(request))


    return render_to_response('items/index.html',
                              {'info': info},
                              context_instance=RequestContext(request))


def details(request, item_id=None):

    def dictToXml(d):
        ret = '<item'
        for k, v in d['item']['attribs'].iteritems():
            ret += ' %s="%s"' % (k, v)
        ret += '>'
        ret += _dictToXml(d['item']['value'])
        ret += '</item>'
        return ret

    def _dictToXml(itemlist):
        ret = ''
        if not isinstance(itemlist, (dict, list)):
            return unicode(itemlist)

        for i in itemlist:
            for k,v in dict(i).iteritems():
                ret += '<%s' % k
                if 'attribs' in v:
                    for attn, attv in v['attribs'].iteritems():
                        ret += ' %s="%s"' % (attn, attv)
                ret += '>'
                ret += _dictToXml(v['value'])
                ret += '</%s>' % k
        return ret

    try:

        item = Item.get(item_id)
        data = dict(item.data)
        xml_data = dictToXml(data)

    except ResourceNotFound:
        item = None

    return render_to_response('items/details.html',
                              {'item': item,
                               'xml_data': xml_data},
                              context_instance=RequestContext(request))

