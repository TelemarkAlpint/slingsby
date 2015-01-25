# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..settings import fix_nonexistent_file_handlers
from .utils import _get_ssh_connection_params, slugify
from .views import ActionView
from .middleware import HttpAcceptMiddleware, HttpMethodOverride

from django.test import TestCase, Client, RequestFactory
from django.http import HttpResponse
from django.template import Template, Context
from mock import Mock

class SettingsTest(TestCase):

    def test_remove_file_handler_nonexisting(self):
        config = {
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',
                },
                'file': {
                    'filename': '/nonexisting/log.log',
                }
            },
            'loggers': {
                'slingsby': {
                    'handlers': ['console', 'file'],
                }
            }
        }
        expected_result = {
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',
                },
                'file': {
                    'filename': 'log.log',
                }

            },
            'loggers': {
                'slingsby': {
                    'handlers': ['console', 'file'],
                }
            }
        }
        fix_nonexistent_file_handlers(config)
        self.assertEqual(expected_result, config)

    def test_remove_file_handler_exists(self):
        config = {
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',
                },
                'file': {
                    'filename': 'log.log',
                }
            },
            'loggers': {
                'slingsby': {
                    'handlers': ['console', 'file'],
                    'level': 'INFO',
                }
            }
        }
        original_config = config.copy()
        fix_nonexistent_file_handlers(config)
        self.assertEqual(config, original_config)

class HttpAcceptMiddlewareTest(TestCase):

    def setUp(self):
        self.request = Mock()
        self.request.META = {}
        self.middleware = HttpAcceptMiddleware()

    def test_normal_accept_header(self):
        self.request.META['HTTP_ACCEPT'] = 'text/html,application/xhtml+xml,application/xml;q=0.9'
        self.middleware.process_request(self.request)
        self.assertTrue(self.request.prefer_html)
        self.assertFalse(self.request.prefer_json)

    def test_missing_accept(self):
        self.middleware.process_request(self.request)
        self.assertTrue(self.request.prefer_html)
        self.assertFalse(self.request.prefer_json)

    def test_want_json(self):
        self.request.META['HTTP_ACCEPT'] = 'text/html;q=0.9,application/json'
        self.middleware.process_request(self.request)
        self.assertFalse(self.request.prefer_html)
        self.assertTrue(self.request.prefer_json)

    def test_equal_priority(self):
        self.request.META['HTTP_ACCEPT'] = 'application/json,text/html'
        self.middleware.process_request(self.request)
        self.assertTrue(self.request.prefer_html)
        self.assertFalse(self.request.prefer_json)

    def test_invalid_accept(self):
        self.request.META['HTTP_ACCEPT'] = 'invalid'
        self.middleware.process_request(self.request)
        self.assertTrue(self.request.prefer_html)
        self.assertFalse(self.request.prefer_json)

    def test_wildcard_accept(self):
        self.request.META['HTTP_ACCEPT'] = '*/*'
        self.middleware.process_request(self.request)
        self.assertTrue(self.request.prefer_html)
        self.assertFalse(self.request.prefer_json)

    def test_jquery_json_accept(self):
        self.request.META['HTTP_ACCEPT'] = 'application/json, text/javascript, */*; q=0.01'
        self.middleware.process_request(self.request)
        self.assertTrue(self.request.prefer_json)
        self.assertFalse(self.request.prefer_html)


class HttpMethodOverrideTest(TestCase):

    def setUp(self):
        self.request = Mock()
        self.middleware = HttpMethodOverride()

    def test_override(self):
        self.request.method = 'POST'
        self.request.POST = {'_http_verb': 'delete'}
        self.middleware.process_request(self.request)
        self.assertEqual(self.request.method, 'delete')

    def test_override_non_post(self):
        self.request.method = 'GET'
        self.request.POST = {'_http_verb': 'delete'}
        self.middleware.process_request(self.request)
        self.assertEqual(self.request.method, 'GET')


class RevvedFileTagTest(TestCase):

    def setUp(self):
        self.filerevs = {'css/styles.css': 'css/styles.cafed00d.css'}

    def test_revved_static_tag(self):
        with self.settings(FILEREVS=self.filerevs):
            template = Template("{% load revved_static %}{% static 'css/styles.css' %}")
            rendered = template.render(Context())
            self.assertEqual(rendered, '/static/css/styles.cafed00d.css')


class StaticRedirectTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_static_redirects(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('cache-control'), 'max-age=0')


class UtilTest(TestCase):

    def test_get_connection_params(self):
        tests = [
            ('localhost', ('vagrant', 'localhost', 22)),
            ('vagrant@localhost:22', ('vagrant', 'localhost', 22)),
            ('travis@127.0.0.1:2222', ('travis', '127.0.0.1', 2222)),
        ]
        for connection_string, expected_result in tests:
            result = _get_ssh_connection_params(connection_string)
            self.assertEqual(result, expected_result)


    def test_slugify(self):
        tests = (
            ("I love it'", 'i-love-it'),
            ("J'ai parlée français, un peu", 'jai-parlee-francais-un-peu'),
            ("Åge og sambandet e hærlig, sjø!, ", 'age-og-sambandet-e-haerlig-sjo'),
            ("Ærlighet varer lengst", 'aerlighet-varer-lengst'),
        )
        for value, expected in tests:
            self.assertEqual(slugify(value), expected)


class ActionViewTest(TestCase):

    def setUp(self):
        class TestView(ActionView):
            actions = ('test',)

            def get(self, request, **kwargs):
                return HttpResponse('GET')

            def test(self, request, **kwargs):
                return HttpResponse('Test')

        self.action_view = TestView.as_view(action='test')
        self.plain_view = TestView.as_view()
        self.rf = RequestFactory()


    def test_get(self):
        request = self.rf.get('/')
        response = self.plain_view(request)
        self.assertEqual(response.status_code, 200)


    def test_action(self):
        request = self.rf.post('/test')
        response = self.action_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Test')


    def test_action_post_only(self):
        request = self.rf.get('/test')
        response = self.action_view(request)
        self.assertEqual(response.status_code, 405)
