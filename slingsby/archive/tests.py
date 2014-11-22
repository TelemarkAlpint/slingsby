from .models import Event, EventForm
from ..general.utils import get_permission

from django.test import Client, TestCase
from django.contrib.auth.models import User
import os.path


class ArchiveEventUploadTest(TestCase):

    def setUp(self):
        self.uploader = Client()
        uploader_user = User.objects.create_user(username='uploader', password='uploaderpw')
        uploader_user.user_permissions = [get_permission('archive.can_upload_images')]
        uploader_user.save()
        self.uploader.login(username='uploader', password='uploaderpw')


    def test_create_new_event(self):
        test_image = os.path.join(os.path.dirname(__file__), 'test-data', '1.jpg')
        with open(test_image, 'rb') as img_fh:
            event_data = {
                'name': 'Skifestivalen',
                'startdate': '2013',
                'images': img_fh,
            }
            response = self.uploader.post('/arkiv/', event_data)
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()

        self.assertEqual(event.name, 'Skifestivalen')
        self.assertEqual(response.status_code, 302)

        # Next upload should not create new event
        test_image2 = os.path.join(os.path.dirname(__file__), 'test-data', '2.jpg')
        with open(test_image2, 'rb') as img_fh:
            event_data = {
                'name': 'Skifestivalen',
                'startdate': '2013',
                'images': img_fh,
            }
            response = self.uploader.post('/arkiv/', event_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.count(), 1)


class ArchiveBaseTest(TestCase):

    def test_valid_event_dates(self):
        invalid_strings = (
            '1976',
            '20014',
            '204-14',
            '2014-1-3',
            '2014-1-12',
            '2014-01-1',
            'aaaa-oo',
            '14-14-13',
            '2014-14-13',
            '2014-10-33',
            '2014-00-12',
            '2016-01-12',
            '2014-10-120',
            '2014-10-12 23:15',
        )
        form_data = {'name': 'Event name'}
        for datestring in invalid_strings:
            form_data.update({'startdate': datestring})
            test_form = EventForm(form_data)
            self.assertFalse(test_form.is_valid())

        valid_strings = (
            '2014',
            '2013-01',
            '1986-01-01',
            '2014-10-12',
            '    2014',
        )
        for datestring in valid_strings:
            form_data.update({'startdate': datestring})
            test_form = EventForm(form_data)
            print str(test_form.errors).decode('utf-8')
            self.assertTrue(test_form.is_valid())


    def test_unauthenticated_archive_access(self):
        response = self.client.post('/arkiv/')
        self.assertEqual(response.status_code, 403)

