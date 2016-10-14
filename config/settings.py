# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os

import environ
import raven


ROOT_DIR = environ.Path(__file__) - 2  # (/a/myfile.py - 2 = /)
APPS_DIR = ROOT_DIR.path('social_auth_proto')

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, 'CHANGEME!!!$n24(@_b545@nu3ojxawr+qk66reidmr&=jld2ied23x2(hpjl'),
    DJANGO_ADMINS=(list, []),
    DJANGO_ALLOWED_HOSTS=(list, []),
    DJANGO_STATIC_ROOT=(str, str(APPS_DIR('staticfiles'))),
    DJANGO_MEDIA_ROOT=(str, str(APPS_DIR('media'))),
    DJANGO_DATABASE_URL=(str, 'postgis:///social_auth_proto'),
    DJANGO_EMAIL_URL=(environ.Env.email_url_config, 'consolemail://user@:password@localhost:25'),
    DJANGO_DEFAULT_FROM_EMAIL=(str, 'admin@example.com'),
    DJANGO_EMAIL_BACKEND=(str, 'django.core.mail.backends.smtp.EmailBackend'),
    DJANGO_SERVER_EMAIL=(str, 'root@localhost.com'),

    SLACK_KEY=(str, ''),
    SLACK_SECRET=(str, ''),
    SLACK_ALLOWED_TEAMS=(list, []),
    DJANGO_CELERY_BROKER_URL=(str, 'redis://localhost:6379/0'),
    DJANGO_CELERY_BACKEND=(str, 'redis://localhost:6379/0'),
    DJANGO_CELERY_ALWAYS_EAGER=(bool, False),

    DJANGO_USE_DEBUG_TOOLBAR=(bool, False),
    DJANGO_TEST_RUN=(bool, False),
)

environ.Env.read_env()

DEBUG = env.bool("DJANGO_DEBUG")

SECRET_KEY = env('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

ADMINS = tuple([tuple(admins.split(':')) for admins in env.list('DJANGO_ADMINS')])

MANAGERS = ADMINS

TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATABASES = {
    'default': env.db('DJANGO_DATABASE_URL')
}

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)

THIRD_PARTY_APPS = (
    'django_extensions',
    'social.apps.django_app.default',
)

LOCAL_APPS = (
    'social_auth_proto.taskapp',
    'social_auth_proto.users',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_USER_MODEL = 'users.User'
ADMIN_URL = r'^admin/'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

EMAIL_URL = env.email_url('DJANGO_EMAIL_URL')
EMAIL_BACKEND = EMAIL_URL['EMAIL_BACKEND']
EMAIL_HOST = EMAIL_URL.get('EMAIL_HOST', '')
if EMAIL_URL.get('EMAIL_HOST_PASSWORD', '') == 'special':
    EMAIL_HOST_PASSWORD = env('DJANGO_EMAIL_HOST_PASSWORD_SPECIAL')
else:
    EMAIL_HOST_PASSWORD = EMAIL_URL.get('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = EMAIL_URL.get('EMAIL_HOST_USER', '')
EMAIL_PORT = EMAIL_URL.get('EMAIL_PORT', '')
EMAIL_USE_SSL = 'EMAIL_USE_SSL' in EMAIL_URL
EMAIL_USE_TLS = 'EMAIL_USE_TLS' in EMAIL_URL
EMAIL_FILE_PATH = EMAIL_URL.get('EMAIL_FILE_PATH', '')

DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = '/static/'
STATIC_ROOT = env('DJANGO_STATIC_ROOT')

MEDIA_URL = '/media/'
MEDIA_ROOT = env('DJANGO_MEDIA_ROOT')

STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# celery settings
BROKER_URL = env('DJANGO_CELERY_BROKER_URL')
CELERY_BACKEND = env('DJANGO_CELERY_BACKEND')
CELERY_ALWAYS_EAGER = env.bool('DJANGO_CELERY_ALWAYS_EAGER')
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_auth_proto.users.backends.CustomSlackOAuth2',
)

SOCIAL_AUTH_SLACK_KEY = env('SLACK_KEY')
SOCIAL_AUTH_SLACK_SECRET = env('SLACK_SECRET')
SOCIAL_AUTH_SLACK_SCOPE = ['identify', 'bot', 'commands', 'users:read', 'chat:write:bot']
SOCIAL_AUTH_SLACK_WHITELISTED_TEAM_NAMES = env('SLACK_ALLOWED_TEAMS')
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
    }
}

if os.environ.get('SENTRY_DSN'):
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)
    RAVEN_CONFIG = {
        'dsn': env('SENTRY_DSN'),
        'release': raven.fetch_git_sha(str(ROOT_DIR)),
    }

if env.bool('DJANGO_USE_DEBUG_TOOLBAR'):
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
    INSTALLED_APPS += ('debug_toolbar', )
    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': [
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ],
        'SHOW_TEMPLATE_CONTEXT': True,
    }

if env.bool('DJANGO_TEST_RUN'):
    pass
