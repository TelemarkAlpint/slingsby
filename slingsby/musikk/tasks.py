# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..general.utils import log_errors, fileserver_ssh_client, upload_file_to_fileserver, slugify
from .models import Song, Vote

from celery import shared_task
from django.conf import settings
from logging import getLogger
import os
import os.path
import shlex
import subprocess


_logger = getLogger('slingsby.musikk.tasks')

# Extension -> CLI args to convert a WAV file into target
WEB_SONG_FORMATS = {
    'mp3': 'lame -V2 --vbr-new %(src)s %(dest)s',
    'ogg': 'sox %(src)s %(dest)s',
}


@shared_task
@log_errors
def process_new_song(song_id):
    """ Takes a raw song uploaded (assumed to be FLAC), converts it into mp3 and ogg,
    pushes it to the fileserver, and updates the song filename and marks it as ready.
    """
    _logger.info('Processing song from celery')
    song = Song.objects.get(pk=song_id)
    try:
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
    except:
        # Reset filename in case of errors, so that admins can try again
        song.filename = ''
        song.save()
        raise


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
    _logger.info('Establishing connection to fileserver to start creating new monday compilation')
    with fileserver_ssh_client() as ssh_client:
        ssh_client.exec_command('python /home/groups/telemark/expeditious/update_top_song.py')
    _logger.info('Compilation created.')


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
