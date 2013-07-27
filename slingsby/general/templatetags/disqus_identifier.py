from django import template

register = template.Library()

@register.filter
def disqus_identifier(value):
    class_name = value.__class__.__name__.lower()
    thing_id = value.id if hasattr(value, 'id') else value['id']
    return 'telemarkalpint-%s-%d' % (class_name, thing_id)
