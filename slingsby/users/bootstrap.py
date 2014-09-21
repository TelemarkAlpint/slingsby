from django.contrib.auth.models import User

def bootstrap():
    User.objects.get_or_create(username='member', email='someone@gmail.nonexistent', password='!')
    User.objects.get_or_create(username='admin', is_staff=True, is_superuser=True,
        email='admin@dev.nonexistent', password='!')
