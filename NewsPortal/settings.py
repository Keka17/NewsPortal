import os.path
from pathlib import Path
import logging

from django.conf.global_settings import DEFAULT_FROM_EMAIL, LOGGING

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-h2u%3+)c_bjis^b3(f)*w4-9xgixzth!1^(j#)4li)78up8yab'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_apscheduler',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.yandex',

    'News',
    'django_filters',
    'rest_framework'
]

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'NewsPortal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',

            ],
        },
    },
]

WSGI_APPLICATION = 'NewsPortal.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Russian')
]

TIME_ZONE = 'UTC'

USE_I18N = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]


USE_TZ = True

STATIC_URL = 'static/'
# Папка, куда collectstatic будет собирать статические файлы
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False

# настройки для верификации email-а
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

ACCOUNT_FORMS = {'signup': 'News.forms.BasicSignupForm'}

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# работает только с VPN

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'charliebrownkb3@gmail.com'
EMAIL_HOST_PASSWORD = 'xiypglkezakcspii'

SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
        # Указываем, куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}




# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'style': '{',
#     'formatters': {
#         'simple_format': {
#             'format': '%(asctime)s %(levelname)s %(message)s'
#         },
#         'verbose_format': {
#             'format': '%(asctime)s %(levelname)s '
#                       '%(message)s %(pathname)s'
#         },
#         'extended_format': {
#             'format': '%(asctime)s %(levelname)s '
#                       '%(message)s %(pathname)s %(exc_info)s '
#         },
#         'module_format': {
#             'format': '%(asctime)s %(levelname)s '
#                       '%(module)s  %(message)s'
#         },
#     },
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',
#         },
#     },
#
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple_format',
#         },
#         'general_file': {
#             'level': 'INFO',
#             'filters': ['require_debug_false'],
#             'class': 'logging.FileHandler',
#             'filename': 'general.log',
#             'formatter': 'module_format',
#         },
#         'verbose_console': {
#             'level': 'WARNING',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose_format',
#         },
#         'extended_console': {
#             'level': 'ERROR',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'extended_format',
#         },
#
#         'errors_file': {
#             'level': 'ERROR',
#             'filters': ['require_debug_true'],
#             'class': 'logging.FileHandler',
#             'filename': 'errors.log',
#             'formatter': 'extended_format',
#         },
#         'security_file': {
#             'level': 'INFO',
#             'filters': ['require_debug_false'],
#             'class': 'logging.FileHandler',
#             'filename': 'security.log',
#             'formatter': 'module_format',
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler',
#             'formatter': 'verbose_format'
#         }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'extended_console', 'general_file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['errors_file', 'mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.server': {
#             'handlers': ['errors_file', 'mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.template': {
#             'handlers': ['errors_file'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.db.backends': {
#             'handlers': ['errors_file'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.security': {
#             'handlers': ['security_file'],
#             'level': 'INFO',
#             'propagate': False,
#
#         }
#     }
# }
