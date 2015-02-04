from django.test import Client, TestCase
from django.contrib.auth.models import User

class ProfilePageTest(TestCase):

    def setUp(self):
        self.anon_user = Client()
        self.logged_in_user = Client()
        User.objects.create_user(username='testuser', password='testpassword')
        self.logged_in_user.login(username='testuser', password='testpassword')


    def test_profile_page(self):
        anon_response = self.anon_user.get('/profil')
        self.assertEqual(anon_response.status_code, 302)

        auth_response = self.logged_in_user.get('/profil')
        self.assertEqual(auth_response.status_code, 200)


class DevLoginTest(TestCase):

    def setUp(self):
        self.client = Client()


    def test_devlogin_in_dev_only(self):
        response = self.client.get('/devlogin')
        self.assertEqual(response.status_code, 404)
