"""
    This script is used to deploy new code to a server, either it's the production server
    or your local copy of it running in vagrant.

    Execute tasks like this:

        $ fab deploy_vagrant

    This will deploy the code built by grunt to your local server.

    To deploy to the production server (note: you don't need to do this manually, travis does
    it for you):

        $ fab deploy -H <username>@ntnuita.no

"""
from fabric.api import run, sudo, put, cd, hosts, env, local
from fabric.context_managers import shell_env
import os
import sys

try:
    import colorama
    colorama.init()
except ImportError:
    if sys.platform.startswith('win'):
        print('Colorama not installed!\n\nIf stuff looks weird you might get better results by ' +
            'running `pip install colorama` first. ')


def deploy():
    """ Package the app and push it to a server.

    Assumes the app has already been built (eg `grunt build`).
    """
    # Push the build artifacts to the server
    put('build/slingsby-1.0.0.tar.gz', '/tmp')
    put('build/static_files.tar.gz', '/tmp')

    # Install the new code
    sudo('/srv/ntnuita.no/venv/bin/pip install -U /tmp/slingsby-1.0.0.tar.gz')
    run('rm /tmp/slingsby-1.0.0.tar.gz')

    # Unpack the static files
    with cd('/srv/ntnuita.no'):
        sudo('tar xf /tmp/static_files.tar.gz -C static')
        sudo('chown -R root:root static')
        sudo('find static -type f -print0 | xargs -0 chmod 644')
        sudo('find static -type d -print0 | xargs -0 chmod 755')
    run('rm /tmp/static_files.tar.gz')
    migrate_db()
    sudo('service uwsgi restart')
    sudo('service slingsby-celery restart')


@hosts('vagrant@127.0.0.1:2222')
def deploy_vagrant():
    """ Shortcut for deploying to vagrant.

    Basically just an alias for `fab deploy -H vagrant:vagrant@localhost:2222
    """
    env.password = 'vagrant'
    deploy()


def migrate_db():
    """ Install and/or migrate the database to the latest version. """
    with shell_env(DJANGO_SETTINGS_MODULE='prod_settings', PYTHONPATH='/srv/ntnuita.no/'):
        sudo('/srv/ntnuita.no/venv/bin/manage.py migrate --noinput', user='uwsgi')


@hosts('vagrant@127.0.0.1:2222')
def bootstrap_vagrant():
    env.password = 'vagrant'
    with shell_env(DJANGO_SETTINGS_MODULE='prod_settings', PYTHONPATH='/srv/ntnuita.no/'):
        sudo('/srv/ntnuita.no/venv/bin/manage.py bootstrap', user='uwsgi')


def provision():
    if not os.path.exists('build'):
        os.mkdir('build')
    local('tar czf build/salt_and_pillar.tar.gz salt pillar')
    put('build/salt_and_pillar.tar.gz', '/tmp')
    sudo('tar xf /tmp/salt_and_pillar.tar.gz -C /srv')
    sudo('salt-call state.highstate --force-color --local')
    sudo('rm /tmp/salt_and_pillar.tar.gz')
