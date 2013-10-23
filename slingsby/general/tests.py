from slingsby.general.middleware import HttpAcceptMiddleware
from slingsby.settings import fix_nonexistent_file_handlers

from django.http import HttpResponse
from django.test import TestCase
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
        response = self.middleware.process_request(self.request)
        self.assertTrue(type(response) == HttpResponse)
        self.assertEqual(response.status_code, 406)
