# -*- coding: utf-8 -*-

from .models import Quote

from django.contrib.webdesign.lorem_ipsum import sentence
from django.contrib.auth.models import User

def bootstrap():
    funny_guy, _ = User.objects.get_or_create(username='funnyguy', first_name='Franko', last_name='Rookie')
    Quote.objects.get_or_create(topic='mandagstrening',
        author='Larsern Rookie',
        suggested_by=funny_guy,
        accepted=True,
        defaults={
            'quote':sentence(),
        }
    )
    Quote.objects.get_or_create(topic='snø',
        author='Petrine',
        suggested_by=funny_guy,
        accepted=True,
        defaults={
            'quote': sentence(),
        }
    )
