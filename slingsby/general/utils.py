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
import shutil


_logger = getLogger(__name__)


@contextmanager
def ignored(*exceptions):
    """ Backport of ignored from python 3.4, use instead of try: risky() except: pass.

    Usage:
        with ignored(OSError):
            os.remove('maybe-present-file')
    """
    try:
        yield
    except exceptions:
        pass


def slugify(text):
    """ Custom slugify that gracefully handles æ, ø and å. """
    text = text.lower().replace('æ', 'ae').replace('ø', 'o').replace('å', 'a')
    return _slugify(text)


def upload_media(src, dest):
    """ Upload a local filename specified by `src` to the fileserver, at path specified by
    `dest`.
    """
    full_dest_path = os.path.join(settings.EXTERNAL_MEDIA_ROOT, dest)
    target_dir = os.path.dirname(full_dest_path)
    old_umask = os.umask(0002)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, 0775)
    shutil.move(src, full_dest_path)
    os.chmod(full_dest_path, 0664)
    os.umask(old_umask)


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
