from django.http import HttpResponse
from users.models import UserProfile, get_full_name
import logging

def add_name_where_missing(request):
    logging.info('Starting to fill in missing names.')
    profiles_without_name = UserProfile.objects.filter(full_name='')
    count = 0
    for profile in profiles_without_name:
        user = profile.user
        full_name = get_full_name(user)
        if full_name:
            profile.full_name = full_name.title()
            profile.save()
            logging.info('Added full name: %s (%s)' % (profile.username, user.email))
            count += 1
    logging.info('Completed adding %d names.' % count)
    return HttpResponse()