from django.core.management.base import NoArgsCommand
import importlib

class Command(NoArgsCommand):
    help = "Create some default objects into a new database"

    def handle_noargs(self, *args, **options):
        from django.conf import settings
        for app in settings.INSTALLED_APPS:
            try:
                bootstrap = importlib.import_module(app + '.bootstrap')
                print('Bootstrapping %s...' % app)
                bootstrap.bootstrap()
            except ImportError:
                pass
