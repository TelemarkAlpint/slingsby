from django.contrib.auth.models import User, Group, Permission

def bootstrap():
    # Create some groups
    arrkom, _ = Group.objects.get_or_create(name='Arrkom')
    arrkom.permissions = [
        Permission.objects.get(codename='add_article'),
        Permission.objects.get(codename='change_article'),
        Permission.objects.get(codename='delete_article'),
        Permission.objects.get(codename='add_event'),
        Permission.objects.get(codename='change_event'),
        Permission.objects.get(codename='delete_event'),
    ]
    styret, _ = Group.objects.get_or_create(name='Styret')
    styret.permissions = [
        Permission.objects.get(codename='approve_song'),
        Permission.objects.get(codename='add_article'),
        Permission.objects.get(codename='change_article'),
        Permission.objects.get(codename='delete_article'),
        Permission.objects.get(codename='add_subpagearticle'),
        Permission.objects.get(codename='change_subpagearticle'),
        Permission.objects.get(codename='delete_subpagearticle'),
        Permission.objects.get(codename='add_event'),
        Permission.objects.get(codename='change_event'),
        Permission.objects.get(codename='delete_event'),
        Permission.objects.get(codename='add_quote'),
        Permission.objects.get(codename='change_quote'),
        Permission.objects.get(codename='delete_quote'),
        Permission.objects.get(codename='approve_quote'),
    ]

    User.objects.get_or_create(username='member', email='someone@gmail.nonexistent', password='!')
    User.objects.get_or_create(username='admin', is_staff=True, is_superuser=True,
        email='admin@dev.nonexistent', password='!')
    styremedlem, _ = User.objects.get_or_create(username='styremedlem', email='styremedlem@ntnuita.local', password='!', is_staff=True)
    styremedlem.groups = [styret]
    styremedlem.save()
    arrkommedlem, _ = User.objects.get_or_create(username='arrkommedlem', email='arrkommedlem@ntnuita.local', password='!', is_staff=True)
    arrkommedlem.groups = [arrkom]
    arrkommedlem.save()
