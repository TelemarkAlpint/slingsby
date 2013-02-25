from django import template

register = template.Library()

@register.filter
def disqus_identifier(value): 
    class_name = value.__class__.__name__.lower()
    return 'telemarkalpint-%s-%d' % (class_name, value.id) 