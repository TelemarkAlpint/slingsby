from ..general.utils import log_errors

from celery import shared_task
from django.contrib.auth.models import User
from django.utils import timezone
from logging import getLogger
import datetime


_logger = getLogger(__name__)


@shared_task
@log_errors
def demote_inactive_users():
    """ Remove membership status for all users which haven't logged in the
    last year.
    """
    _logger.info('Starting demotion of inactive users')
    cutoff_time = timezone.now() - datetime.timedelta(days=365)
    inactive_users = User.objects.filter(last_login__lte=cutoff_time)
    for inactive_user in inactive_users:
        inactive_user.profile.member_since = None
        inactive_user.profile.save()
