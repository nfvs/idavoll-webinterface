from django import template

from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode


register = template.Library()

def update_page(get, args=None):
    print 'GET: "%s"' % get
    print 'TYPE: %s' % type(get)
    """
    i = get.get('page')
    if args == "previous":
        get.update({'page': i+1})
    else:
        get.update({'page': i-1})
    """
    return get


def unordered_list_hl(value, args=None):
    autoescape = None
    """
    Recursively takes a self-nested list and returns an HTML unordered list --
    WITHOUT opening and closing <ul> tags.

    The list is assumed to be in the proper format. For example, if ``var``
    contains: ``['States', ['Kansas', ['Lawrence', 'Topeka'], 'Illinois']]``,
    then ``{{ var|unordered_list }}`` would return::

        <li>States
        <ul>
                <li>Kansas
                <ul>
                        <li>Lawrence</li>
                        <li>Topeka</li>
                </ul>
                </li>
                <li>Illinois</li>
        </ul>
        </li>
    """
    arg_list = [arg for arg in args.split(',')]
    arg_name = arg_list[0]
    arg_id = arg_list[1]
    
    if autoescape:
        from django.utils.html import conditional_escape
        escaper = conditional_escape
    else:
        escaper = lambda x: x
    def convert_old_style_list(list_):
        """
        Converts old style lists to the new easier to understand format.

        The old list format looked like:
            ['Item 1', [['Item 1.1', []], ['Item 1.2', []]]

        And it is converted to:
            ['Item 1', ['Item 1.1', 'Item 1.2]]
        """
        if not isinstance(list_, (tuple, list)) or len(list_) != 2:
            return list_, False
        first_item, second_item = list_
        if second_item == []:
            return [first_item], True
        old_style_list = True
        new_second_item = []
        for sublist in second_item:
            item, old_style_list = convert_old_style_list(sublist)
            if not old_style_list:
                break
            new_second_item.extend(item)
        if old_style_list:
            second_item = new_second_item
        return [first_item, second_item], old_style_list
    def _helper(list_, tabs=1):
        indent = u'\t' * tabs
        output = []

        list_length = len(list_)
        i = 0
        while i < list_length:
            # NFVS
            #title = list_[i]
            title_n = getattr(list_[i], arg_name)
            title_i = getattr(list_[i], arg_id)
            title = '<a href="%s/">%s</a>' % (title_i, title_n)
            sublist = ''
            sublist_item = None
            if isinstance(title, (list, tuple)):
                sublist_item = title
                title = ''
            elif i < list_length - 1:
                next_item = list_[i+1]
                if next_item and isinstance(next_item, (list, tuple)):
                    # The next item is a sub-list.
                    sublist_item = next_item
                    # We've processed the next item now too.
                    i += 1
            if sublist_item:
                sublist = _helper(sublist_item, tabs+1)
                sublist = '\n%s<ul>\n%s\n%s</ul>\n%s' % (indent, sublist,
                                                         indent, indent)
            output.append('%s<li>%s%s</li>' % (indent,
                    escaper(force_unicode(title)), sublist))
            i += 1
        return '\n'.join(output)
    value, converted = convert_old_style_list(value)
    return mark_safe(_helper(value))
unordered_list_hl.is_safe = True
#unordered_list_hl.needs_autoescape = True

update_page.is_safe = True

register.filter('unordered_list_hl', unordered_list_hl)
register.filter('update_page', update_page)