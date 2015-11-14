from ..general.utils import get_permission

from django.contrib.auth.models import User, Group


def bootstrap():
    # Create some groups
    arrkom, _ = Group.objects.get_or_create(name='Arrkom')
    arrkom.permissions = [
        get_permission('articles.add_article'),
        get_permission('articles.change_article'),
        get_permission('articles.delete_article'),
        get_permission('events.add_event'),
        get_permission('events.change_event'),
        get_permission('events.delete_event'),
        get_permission('events.early_signup'),
        get_permission('events.add_signup'),
        get_permission('events.change_signup'),
        get_permission('events.delete_signup'),
    ]
    styret, _ = Group.objects.get_or_create(name='Styret')
    styret.permissions = [
        get_permission('musikk.approve_song'),
        get_permission('articles.add_article'),
        get_permission('articles.change_article'),
        get_permission('articles.delete_article'),
        get_permission('articles.add_subpagearticle'),
        get_permission('articles.change_subpagearticle'),
        get_permission('articles.delete_subpagearticle'),
        get_permission('events.add_event'),
        get_permission('events.change_event'),
        get_permission('events.delete_event'),
        get_permission('events.early_signup'),
        get_permission('events.add_signup'),
        get_permission('events.change_signup'),
        get_permission('events.delete_signup'),
        get_permission('quotes.add_quote'),
        get_permission('quotes.change_quote'),
        get_permission('quotes.delete_quote'),
        get_permission('quotes.approve_quote'),
    ]

    User.objects.get_or_create(username='member', email='someone@gmail.nonexistent', password='!')
    User.objects.get_or_create(username='admin', is_staff=True, is_superuser=True,
        email='admin@dev.nonexistent', password='!')
    styremedlem, _ = User.objects.get_or_create(username='styremedlem',
        email='styremedlem@ntnuita.local', password='!', is_staff=True)
    styremedlem.groups = [styret]
    styremedlem.save()
    arrkommedlem, _ = User.objects.get_or_create(username='arrkommedlem',
        email='arrkommedlem@ntnuita.local', password='!', is_staff=True)
    arrkommedlem.groups = [arrkom]
    arrkommedlem.save()
