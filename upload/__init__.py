# coding: utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.safestring import SafeUnicode
from django.views.generic.simple import direct_to_template
from events.models import Event, EventFullException, \
    UserAlreadyRegisteredException
from general import cache, feedback, reverse_with_params, add_params
from quotes.models import QuoteForm
from musikk.models import SongSuggestionForm, ReadySongForm, Song
from simple_forum.models import CategoryForm, PostForm
from users.models import UserProfileForm
import logging

logger = logging.getLogger(__name__)

def upload_category(request):
    return upload(request, CategoryForm, reverse('upload.upload_category'), reverse('forum'))

def upload_post(request):
    return upload(request, PostForm, reverse('upload.upload_post'), reverse('forum'))

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

def toggle_event_participation(request):
    redirect = request.POST.get('redirect', 'program')
    event = Event.objects.get(id=request.POST['event_id'])
    user = request.user
    if event.is_user_participant(user):
        if not event.binding_registration:
            event.remove_user(user)
            redirect = add_params(redirect,
                                  feedback.EVENT_SIGN_OFF.format_string(event))
            logger.info('%s meldte seg av eventet %s.', user, event)
        else:
            logger.warning('%s tried to unregister from the binding event "%s"' % (user.username, event.name))
            logger.warning('Current POST data: %s' % str(request.POST))
            return direct_to_template(request, 'infopage.html',
                                        {'content': SafeUnicode('''Beklager, men dette eventet har bindende p&aring;melding. Ta
                                        kontakt med arrkom hvis du absolutt ikke har mulighet til &aring; stille,
                                        s&aring; vil vi se om vi kan gj&oslash;re noe med det.''')})
    else:
        try:
            event.add_user(user)
            redirect = add_params(redirect, feedback.EVENT_SIGN_ON.format_string(event))
            logger.info('%s meldte seg på eventet %s.', user, event)
        except (EventFullException, UserAlreadyRegisteredException) as e:
            logger.warning(e.message)
    return HttpResponseRedirect('/%s' % redirect)
