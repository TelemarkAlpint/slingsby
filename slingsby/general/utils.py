# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from collections import namedtuple
from contextlib import contextmanager
from django.conf import settings
from django.utils.text import slugify as _slugify
from functools import wraps
from logging import getLogger
from urlparse import urlparse
import mock
import os
import paramiko
import StringIO


_logger = getLogger(__name__)


def slugify(text):
    """ Custom slugify that gracefully handles æ, ø and å. """
    text = text.lower().replace('æ', 'ae').replace('ø', 'o').replace('å', 'a')
    return _slugify(text)


def get_permission(label):
    # Late import these so that the module can be imported in the settings
    from django.contrib.auth.models import Permission
    app, codename = label.split('.')
    potential_permissions = Permission.objects.filter(codename=codename)
    for permission in potential_permissions:
        if permission.content_type.app_label == app:
            return permission
    raise ValueError('No such permission: %s' % label)


@contextmanager
def disconnect_signal(signal, sender):
    """ Use as a context manager to prevent signals from being run for some time:

        with disconnect_signal(pre_save, sender=MyModel):
            do_stuff_without_signal_interfering()
    """
    receivers = signal.receivers
    signal.receivers = []
    yield
    signal.receivers = receivers


def log_errors(func):
    """ Decorator to wrap a function in a try/except, and log errors. """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except: # pylint: disable=bare-except
            _logger.exception("Task failed!")
            raise
    return wrapper


class MockSSHClient(mock.Mock):
    """ Mock SSH client that can be used in tests. """

    def open_sftp(self):
        print 'Opening sftp!'
        return self


    def put(self, source, dest):
        """ Run SFTP file uploads locally. """
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
        with open(source, 'rb') as source_fh:
            with open(dest, 'wb') as dest_fh:
                dest_fh.write(source_fh.read())


@contextmanager
def fileserver_ssh_client():
    """ Context-manager to get ssh connection to the fileserver. """
    ssh_client = None
    try:
        ssh_client = _get_ssh_client()
        _logger.info('SSH connection to fileserver established')
        yield ssh_client
    finally:
        if ssh_client:
            ssh_client.close()
            _logger.info('SSH connection to filserver closed')


def upload_file_to_fileserver(ssh_client, src, dest):
    """ Uploads a file to the media dir on the remote fileserver.

    Src path must either be absolute or relative to MEDIA_ROOT.
    """
    # We assume that the target fileserver is always running linux, but the local
    # machine might be running windows, so we can't use the os.path module for
    # path manipulation, as it would use the separator from the local machine.
    fileserver_media_root = settings.FILESERVER_MEDIA_ROOT
    if not fileserver_media_root[-1] == '/':
        fileserver_media_root += '/'
    dest = fileserver_media_root + dest
    media_src = os.path.join(settings.MEDIA_ROOT, src)
    _logger.info('Uploading file to fileserver: %s, dest: %s', media_src, dest)
    target_dir = os.path.dirname(dest)
    # umask to make dirs 775 so that future telemark admins can use them as well
    command = 'test -d {0} || (umask 002 && mkdir -p {0} && chmod g+s {0})'.format(target_dir)
    ssh_client.exec_command(command)
    sftp = ssh_client.open_sftp()
    sftp.put(media_src, dest)
    # Make sure future telemark admins have sufficient permissions:
    sftp.chmod(dest, 0664)
    _logger.info('File upload completed')


def _get_ssh_client():
    if hasattr(settings, 'SSH_CLIENT') and settings.SSH_CLIENT:
        return settings.SSH_CLIENT
    else:
        return _get_paramiko_ssh_client()


def _get_paramiko_ssh_client():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    temp_key = StringIO.StringIO(settings.FILESERVER_KEY)
    pkey = paramiko.RSAKey.from_private_key(temp_key)
    temp_key.close()
    connection = _get_ssh_connection_params(settings.FILESERVER)
    _logger.info('Establishing SSH connection to %s, pkey=%s', connection, temp_key)
    ssh.connect(connection.host, port=connection.port, username=connection.user,
        pkey=pkey, look_for_keys=False)
    return ssh


def _get_ssh_connection_params(conn_str):
    """ Extract user, host and port from a string like 'vagrant@localhost:2222'.
    Returns a namedtuple (user, host, port).

    Defaults to user 'vagrant' and port 22 if not specified in the string.
    """
    Connection = namedtuple('Connection', ['user', 'host', 'port']) # pylint: disable=invalid-name
    default_port = 22
    default_username = 'vagrant'
    parts = urlparse('ssh://' + conn_str)
    return Connection(parts.username or default_username,
        parts.hostname,
        parts.port or default_port)
