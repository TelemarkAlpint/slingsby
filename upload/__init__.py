# coding: utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.safestring import SafeUnicode
from django.views.generic.simple import direct_to_template
from general import cache, feedback, reverse_with_params, add_params
from quotes.models import QuoteForm
from musikk.models import SongSuggestionForm, ReadySongForm, Song
from users.models import UserProfileForm
import logging

logger = logging.getLogger(__name__)

def upload_quote(request):
    redirect = reverse_with_params(feedback_code=feedback.QUOTE_THANKS)
    return upload(request, QuoteForm, reverse('upload.upload_quote'), redirect)

def upload(request, model_form, upload_handler_url, redirect='/', instance=None,
           post_save=None, custom_log=None, *args, **kwargs):
    if request.method == 'POST':
        if instance is None:
            form = model_form(request.POST)
        else:
            form = model_form(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            class_name = instance.__class__.__name__.lower()
            form.save()
            if not custom_log:
                logging.info('%s lastet opp %s: %s', request.user.profile.username, class_name, instance)
#                logging.info(request.user, UPLOADED_OBJECT, class_name, instance)
            else:
                logging.info(custom_log, request.user.profile.username, *args, **kwargs)
            if post_save is not None:
                post_save()
            return HttpResponseRedirect(redirect)
        logging.info('Invalid form, trying again...')
    else:
        form = model_form()
    values = {'form': form, 'upload_handler_url': upload_handler_url}
    return direct_to_template(request, 'invalid_form.html', values)

def submit_full_name(req):
    inst = req.user.profile
    redir = reverse_with_params('profil', feedback.NAME_COMP)
    return upload(req, UserProfileForm, reverse('submit_full_name'), redir, inst)