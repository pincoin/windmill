from django.conf import settings

DISALLOWED_EMAIL_DOMAIN = getattr(settings, 'DISALLOWED_EMAIL_DOMAIN', (
    'qq.com', '163.com', '126.com', '188.com', 'yeah.net', 'sina.com'
))

DAYS_LOGIN_RECPATCHA = getattr(settings, 'DAYS_LOGIN_RECPATCHA', 365)

GOOGLE_RECAPTCHA_SESSION_KEY = getattr(settings, 'GOOGLE_RECAPTCHA_SESSION_KEY', 'GOOGLE_RECAPTCHA')
