from slingsby.settings import fix_nonexistent_file_handlers

from django.test import TestCase

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
