from django import template

register = template.Library()

@register.filter
def shorten(text, num_chars):
    """ Split a long text in two parts and add ellipses in between.

    Ex: "My long text this is" -> "My lo...is is!"
    """
    if len(text) > num_chars and num_chars > 5:
        padding = num_chars // 2
        ellipses = unichr(8230) # Horizontal ellipses
        shortened = text[:padding] + ellipses + text[-padding+1:]
        return shortened
    else:
        return text

@register.filter
def truncatechars(text, num_chars):
    if len(text) > num_chars:
        return text[:num_chars - 1] + unichr(8230)
    else:
        return text
