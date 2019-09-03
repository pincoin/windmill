from django.utils.translation import ugettext_lazy as _

from .base import *

DEBUG = True

# Internationalization
LANGUAGE_CODE = 'ko-KR'
LANGUAGES = [
    ('ko', _('Korean')),
    ('th', _('Thai')),
    ('en', _('English')),
]
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'Asia/Bangkok'

# Static files (CSS, Javascript, Images)
STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'conf', 'static'),
    os.path.join(BASE_DIR, 'golf', 'static'),
    os.path.join(BASE_DIR, 'member', 'static'),
]

# Media files (Uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# django.contrib.sites settings for allauth
SITE_ID = 1

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 300,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'conf': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'golf': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'member': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}
