from django import template

register = template.Library()

@register.filter
def change_base(value, bases):
    """ Converts a string in a given base to a target base.

    Bases argument should be a a string in the format 'from,to'.

    If base > 16, the conversion is not well defined, as it's not clear which symbols to use. """

    src_base, target_base = [int(s) for s in bases.split(',')]
    if isinstance(value, int):
        num = value
    else:
        num = int(value, base=src_base)

    if target_base == 2:
        return '{0:b}'.format(num)
    elif target_base == 8:
        return '{0:o}'.format(num)
    elif target_base == 10:
        return '{}'.format(num)
    elif target_base == 16:
        return '{0:x}'.format(num)
    else:
        chars = '0123456789abcdef'
        result = []
        div = abs(num)
        while div:
            div, mod = divmod(div, target_base)
            result.append(chars[mod])
            if div == 0:
                break
        if num < 0:
            result.append('-')
        return ''.join(reversed(result))
