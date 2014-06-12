# -*- coding: utf-8 -*-
""" Add a couple of example articles. """

from .models import Article, SubPageArticle
from ..general.time import now

from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.webdesign.lorem_ipsum import paragraphs

def bootstrap():
    johnny, _ = User.objects.get_or_create(username='johnnydev', first_name='Johnny', last_name='Dev')
    pedro, _ = User.objects.get_or_create(username='pedro', first_name='Pedro', last_name='Trenersjef')
    Article.objects.get_or_create(title='Ny funksjonalitet på nettsidene oppe snart',
        content='''<p>
                Masse nye spennende greier på vei, dette blir kult.
            </p>
            <h2>Nye greier</h2>
            <p>Noen av de nye greiene som kommer er:</p>
            <ul>
                <li>Awesomeness</li>
                <li>Kule ting</li>
                <li>Buzzwords</li>
                <li>Puddergaranti</li>
            </ul>
            <p>
                Håper endringene faller i smak!
            </p>''',
        author=johnny,
        defaults={
            'published_date': now(),
        }
    )

    Article.objects.get_or_create(title='Trening starter på igjen NÅ!',
        content='''<p>
                Mandagstrening is back in the groove, snakkes på i-bygget!
            </p>
            <p>
                Se treningssiden for mer info hvis du trenger det, men dette burde dekke det meste.
            </p>''',
        author=pedro,
        defaults={
            'published_date': (now() - timedelta(days=1)),
        }
    )

    for i in range(15):
        Article.objects.get_or_create(title='Tilfeldig sluddervarv #%d' % i,
            author=johnny,
            defaults={
                'published_date': (now() - timedelta(days=(2 + i))),
                'content': ''.join('<p>%s</p>' % p for p in paragraphs(3)),
            }

        )

    SubPageArticle.objects.get_or_create(title='Trening',
        slug='trening',
        content='''<p>
                Vi trener sånn innimellom, stort sett på mandager, stort sett i 20-tiden.
            </p>
            <p>
                Du finner oss i I-bygget på Gløs.
            </p>''',
        author=pedro,
        defaults={
            'published_date': (now() - timedelta(hours=3)),
        }
    )

    SubPageArticle.objects.get_or_create(title='Webutvikling',
        slug='webutvikling',
        content='''<p>
                Trenger stadig nye sjeler til å bidra med webutvikling, har du noe fornuftig å
                komme med er det bare å skrike ut.
            </p>''',
        author=johnny,
        defaults={
            'published_date': (now() - timedelta(hours=5)),
        }
    )
