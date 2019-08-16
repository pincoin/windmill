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
TIME_ZONE = 'UTC'

# Static files (CSS, Javascript, Images)
STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'conf', 'static'),
]

# Media files (Uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

SITE_ID = 1
