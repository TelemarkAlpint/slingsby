from django.core import mail
from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.loader import get_template

def send_templated_mail(subject, template, recipient_list, context=None, **kwargs):
    if context is None:
        context = {}
    plaintext_template = get_template(template + '.txt')
    html = None
    try:
        html_template = get_template(template + '.html')
        html = html_template.render(context)
    except TemplateDoesNotExist:
        pass
    plaintext = plaintext_template.render(context)

    return mail.send_mail(subject=subject, message=plaintext,
        from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=recipient_list,
        html_message=html, **kwargs)
