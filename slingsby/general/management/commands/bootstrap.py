from __future__ import print_function

from slingsby.general.utils import ignored

from django.core.management.base import BaseCommand, CommandError
import importlib

class Command(BaseCommand):
    """ Bootstrap all or just some modules by running the bootstrap function found in
    their bootstrap module.
    """
    args = '[app_label app_label ...]'

    def handle(self, *app_labels, **options):
        from django.apps import apps
        if not app_labels:
            app_labels = []
        try:
            app_configs = [apps.get_app_config(app_label) for app_label in app_labels]
        except (LookupError, ImportError) as ex:
            raise CommandError("%s. Are you sure your INSTALLED_APPS setting is correct?" % ex)
        if not app_configs:
            bootstrap_all()
        else:
            for app_config in app_configs:
                bootstrap_single(app_config.name)


def bootstrap_all(*args, **options):
    from django.conf import settings
    for app in settings.INSTALLED_APPS:
        with ignored(ImportError):
            bootstrap_single(app)


def bootstrap_single(app):
    bootstrap_mod = importlib.import_module(app + '.bootstrap')
    print('Bootstrapping %s...' % app)
    bootstrap_mod.bootstrap()
