# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..general.utils import log_errors, slugify, fileserver_ssh_client, upload_media
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
    # Make sure new files and directories are created with correct permissions
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
        for converted_file in converted_files:
            extension = os.path.splitext(converted_file)[1]
            new_filename = new_basename + extension
            upload_media(converted_file, new_filename)
        song.ready = True
        song.save()
    except:
        # Reset filename in case of errors, so that admins can try again
        song.filename = ''
        song.save()
        raise


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
    target_folder = os.path.join(settings.MEDIA_ROOT, 'local', 'musikk')
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    converted = []
    for extension, cli_call in WEB_SONG_FORMATS.items():
        new_filename = '%s.%s' % (basename, extension)
        dest = os.path.join(target_folder, new_filename)
        command = cli_call % {'src': src_path, 'dest': dest}
        args = _get_subprocess_args(command)
        _logger.debug("New file: %s", new_filename)
        subprocess.check_call(args)
        converted.append(dest)
    return converted


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
    temp_dir = tempfile.mkdtemp()
    _logger.debug('Creating new song compilation, temp_dir is %s' % temp_dir)
    silence_file = generate_silence_file(temp_dir)
    urls = get_song_urls()
    files = fetch_songs(temp_dir, urls)
    wav = merge_files(files, silence_file)
    mp3 = convert_to_mp3(wav)
    metadata = write_metadata(mp3, urls)
    _logger.debug('Done. Completed mp3 is here: %s' % mp3)
    os.remove(wav)
    shutil.rmtree(temp_dir)


def generate_silence_file(temp_dir):
    _logger.debug('Creating silence file...')
    filename = os.path.join(temp_dir, 'silence.wav')
    subprocess.check_call(['sox', '-n', '-r', '44100', '-c', '2', filename, 'trim', '0.0', '15.0'])
    _logger.debug('Silence created.')
    return filename


def get_song_urls():
    _logger.debug('Fetching top song list...')
    response = requests.get('http://ntnuita.no/musikk/top/list/')
    response.raise_for_status()
    song_data = response.json()
    song_list = song_data['songs']
    url_list = [song['filename'] + '.ogg' for song in song_list]
    _logger.debug('%d songs found.' % len(url_list))
    return url_list


def fetch_songs(temp_dir, song_urls):
    files = []
    for song_num, song_url in enumerate(song_urls, 1):
        target_file = os.path.join(temp_dir, str(song_num) + '.ogg')
        with open(target_file, 'w') as fh:
            _logger.debug('Downloading song %s' % song_url)
            response = requests.get(song_url, stream=True)
            response.raise_for_status()
            for block in response.iter_content(1024):
                if not block:
                    break
                fh.write(block)
        files.append(target_file)
    return files


def merge_files(files, silence_file):
    _logger.debug('Merging files...')
    target = get_new_filename()
    command = ['sox']
    for song_file in files:
        if sys.version_info > (3, 0, 0):
            command.append(song_file)
        else:
            # Python2, wtf?
            command.append(song_file.encode('latin-1'))
        command.append(silence_file)
    command.append(target)
    subprocess.check_call(command)
    return target


def get_new_filename():
    todays_date = datetime.now().strftime('%Y.%m.%d')
    return '%s.wav' % todays_date


def convert_to_mp3(source):
    _logger.debug('Converting merged file to mp3...')
    dest = path.splitext(source)[0] + '.mp3'
    subprocess.check_call([lame, '-V2', '--vbr-new', '--tt', 'Mandagstrening', '--ta',
        'NTNUI Telemark-Alpint', '--ty', str(datetime.now().year), '--tc',
        'Generert %s' % datetime.now().strftime('%Y-%m-%d %H:%M'), '--tl', 'Best of I-bygget',
        source, dest])
    return dest


def write_metadata(filename, urls):
    """ Write file used to recreate the file, or see the songs it contains. """
    song_meta_filename = path.splitext(filename)[0] + '.json'
    creation_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    song_meta = {
        'created': creation_time,
        'filename': filename,
        'songs': [{'filename': path.splitext(url)[0]} for url in urls],
    }
    with open(song_meta_filename, 'w') as song_meta_fh:
        json.dump(song_meta, song_meta_fh, indent=2)
    return song_meta_filename
    _logger.debug('Compilation created.')


def _get_subprocess_args(args_str):
    """ From a string of CLI args, like 'ls -l', convert it to something that can be passed to
    subprocess.check_call(). For windows, this is the same as the input, for *nix it's passed
    through shlex.split() -> ['ls', '-l'].
    """
    if os.name == 'nt': # pragma: no-cover
        return args_str
    else:
        return shlex.split(args_str)
