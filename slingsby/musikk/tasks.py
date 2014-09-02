# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .models import Song, Vote

from celery import shared_task
from collections import namedtuple
from contextlib import contextmanager
from django.conf import settings
from functools import wraps
from logging import getLogger
from urlparse import urlparse
import os
import os.path
import paramiko
import re
import shlex
import StringIO
import subprocess
import unicodedata


_logger = getLogger('slingsby.musikk.tasks')

# Extension -> CLI args to convert a WAV file into target
WEB_SONG_FORMATS = {
    'mp3': 'lame -V2 --vbr-new %(src)s %(dest)s',
    'ogg': 'sox %(src)s %(dest)s',
}


def slugify(text):
    """ Custom slugify that gracefully handles æ, ø and å.

    Otherwise identical to django.utils.text.slugify.
    """
    text = text.replace('æ', 'ae').replace('ø', 'o').replace('å', 'a')
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)


@contextmanager
def fileserver_ssh_client():
    """ Context-manager to get ssh connection to the fileserver. """
    ssh_client = None
    try:
        ssh_client = get_ssh_client()
        _logger.info('SSH connection to fileserver established')
        yield ssh_client
    finally:
        if ssh_client:
            ssh_client.close()
            _logger.info('SSH connection to filserver closed')


def log_errors(func):
    """ Decorator to wrap a function in a try/except, and log errors. """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except: # pylint: disable=bare-except
            _logger.exception("Task failed!")

    return wrapper


@shared_task
@log_errors
def process_new_song(song_id):
    """ Takes a raw song uploaded (assumed to be FLAC), converts it into mp3 and ogg,
    pushes it to the fileserver, and updates the song filename and marks it as ready.
    """
    _logger.info('Processing song from celery')
    song = Song.objects.get(pk=song_id)
    src_file = str(song.filename)
    wav_file = to_wav(src_file)
    _logger.debug('Wav file: %s', wav_file)
    converted_files = convert_file(wav_file)
    _logger.debug('Converted files: %s', converted_files)
    os.remove(wav_file)
    new_basename = '/'.join(['musikk', slugify(song.artist), slugify(song.title)])
    _logger.debug('New basename for song is %s', new_basename)
    song.filename = new_basename
    with fileserver_ssh_client() as ssh_client:
        for converted_file in converted_files:
            extension = os.path.splitext(converted_file)[1]
            new_filename = new_basename + extension
            upload_file_to_fileserver(ssh_client, converted_file, new_filename)
    song.ready = True
    song.save()


@shared_task
@log_errors
def count_votes():
    """ Count up all new votes and recalculate song ratings. """
    from .views import _EXPONENTIAL_BASE
    _logger.info('Starting to count new votes...')
    all_songs = list(Song.objects.all())
    votes = Vote.objects.select_related('song').filter(counted=False)
    max_rating = 0.0
    vote_array = []
    for vote in votes:
        vote_array.append(vote.song.id)
        vote.counted = True
        vote.save()
    _logger.info('%d new votes found.', len(vote_array))
    for song in all_songs:
        for voted_song in vote_array:
            if voted_song == song.id:
                song.votes += 1
            else:
                song.votes *= _EXPONENTIAL_BASE
        if song.votes > max_rating:
            max_rating = song.votes
    for song in all_songs:
        song.popularity = song.votes * 100 / max_rating
        song.save()
    _logger.info('All votes counted.')


@shared_task
@log_errors
def create_new_compilation():
    """ Creates a new song for monday excercise, merging all the top-rated ones. """
    print('Establishing connection to fileserver to start creating new monday compilation')
    with fileserver_ssh_client() as ssh_client:
        ssh_client.exec_command('python /home/groups/telemark/expeditious/update_top_song.py')
    print('Compilation created.')


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
    # umask to make dirs 775 such that future telemark admins can use them as well
    ssh_client.exec_command('test -d {0} || (umask 002 && mkdir -p {0} && chmod g+s {0})'.format(target_dir))
    sftp = ssh_client.open_sftp()
    sftp.put(media_src, dest)
    # Make sure future telemark admins have sufficient permissions:
    sftp.chmod(dest, 0664)
    _logger.info('File upload completed')


def get_ssh_client():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    temp_key = StringIO.StringIO(settings.FILESERVER_KEY)
    pkey = paramiko.RSAKey.from_private_key(temp_key)
    temp_key.close()
    connection = get_ssh_connection_params(settings.FILESERVER)
    ssh.connect(connection.host, port=connection.port, username=connection.user,
        pkey=pkey)
    return ssh


def get_ssh_connection_params(conn_str):
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


def to_wav(src_path):
    """ Takes a file like `loose_yourself-raw.flac` and converts it into `loose_yourself.wav`.

    Path must be either absolute or relative to MEDIA_ROOT."""
    _logger.debug('Converting %s to wav..', src_path)
    new_filename = src_path[:src_path.rindex('-raw')] + '.wav'
    src_path = os.path.join(settings.MEDIA_ROOT, src_path)
    new_path = os.path.join(settings.MEDIA_ROOT, new_filename)
    command = ['sox', src_path, new_path]
    subprocess.check_call(command)
    return new_path


def convert_file(src_path):
    """ Converts a WAV file into mp3 and ogg (web versions) """
    filename = os.path.split(src_path)[1]
    basename = os.path.splitext(filename)[0]
    target_folder = os.path.join(settings.MEDIA_ROOT, 'musikk')
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    converted = []
    for extension, cli_call in WEB_SONG_FORMATS.items():
        new_filename = '%s.%s' % (basename, extension)
        dest = os.path.join(target_folder, new_filename)
        command = cli_call % {'src': src_path, 'dest': dest}
        args = _get_subprocess_args(command)
        _logger.info("New file: %s", new_filename)
        subprocess.check_call(args)
        converted.append(dest)
    return converted


def _get_subprocess_args(args_str):
    """ From a string of CLI args, like 'ls -l', convert it to something that can be passed to
    subprocess.check_call(). For windows, this is the same as the input, for *nix it's passed
    through shlex.split() -> ['ls', '-l'].
    """
    if os.name == 'nt':
        return args_str
    else:
        return shlex.split(args_str)
