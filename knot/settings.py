# Copyright [2019] [FORTH-ICS]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Django settings for knot project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET', '%ad&%4*!xpf*$wd3^t56+#ode4=@y^ju_t+j9f+20ajsta^gog')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv('DJANGO_DEBUG', '1') else False

ALLOWED_HOSTS = ['*']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_SCHEME', 'https')


# Version
try:
    with open(os.path.join(BASE_DIR, 'VERSION'), 'rb') as f:
        VERSION = f.read().decode().strip().lstrip('v')
except:
    raise
    VERSION = 'unknown'


# Application definition

INSTALLED_APPS = [
    'dashboard.apps.DashboardConfig',
    'crispy_forms',
    'impersonate',
    'chunked_upload',
    'oauth2_provider',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
    'dashboard.middleware.ProxyUserMiddleware',
    'knot.middleware.AddLogUserHeaderMiddleware',
]

ROOT_URLCONF = 'knot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dashboard.context_processors.settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'knot.wsgi.application'
ASGI_APPLICATION = 'knot.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# Password hashes

PASSWORD_HASHERS = [
    'dashboard.hashers.APR1PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASE_DIR = os.getenv('KNOT_DATABASE_DIR', os.path.join(BASE_DIR, 'db'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATABASE_DIR, 'db.sqlite3'),
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Authentication

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

LDAP_SERVER_URL = os.getenv('KNOT_LDAP_SERVER_URL')
if LDAP_SERVER_URL:
    import json

    from urllib.parse import urlparse

    ldap_server_url = urlparse(LDAP_SERVER_URL)
    ldap_server_netloc = '%s:%s' % (ldap_server_url.hostname, ldap_server_url.port) if ldap_server_url.port else ldap_server_url.hostname

    AUTH_LDAP_SERVER_URI = ldap_server_url._replace(netloc=ldap_server_netloc).geturl()
    AUTH_LDAP_BIND_DN = ldap_server_url.username
    AUTH_LDAP_BIND_PASSWORD = ldap_server_url.password
    AUTH_LDAP_USER_DN_TEMPLATE = os.getenv('KNOT_LDAP_USER_DN_TEMPLATE')
    AUTH_LDAP_USER_ATTR_MAP = json.loads(os.getenv('KNOT_LDAP_USER_ATTR_MAP'))
    # AUTH_LDAP_ALWAYS_UPDATE_USER = True

    AUTHENTICATION_BACKENDS += ['django_auth_ldap.backend.LDAPBackend']


# Enable OIDC

OIDC_RSA_PRIVATE_KEY_FILE = os.path.join(DATABASE_DIR, 'oidc.key')
# Check for the database dir to avoid creating the key in the container image.
if os.path.exists(DATABASE_DIR) and not os.path.exists(OIDC_RSA_PRIVATE_KEY_FILE):
    if os.system('openssl genrsa -out %s 4096' % OIDC_RSA_PRIVATE_KEY_FILE) != 0:
        raise SystemError('Can not create private key for OIDC')

if os.path.exists(OIDC_RSA_PRIVATE_KEY_FILE):
    with open(OIDC_RSA_PRIVATE_KEY_FILE) as f:
        OIDC_RSA_PRIVATE_KEY = f.read()

    OAUTH2_PROVIDER = {
        "OIDC_ENABLED": True,
        "OIDC_RSA_PRIVATE_KEY": OIDC_RSA_PRIVATE_KEY,
        "OAUTH2_VALIDATOR_CLASS": "dashboard.oauth_validators.CustomOAuth2Validator",
        "SCOPES": { # Scopes requested by social_core.backends.django.DjangoOpenIdConnect
            "openid": "OpenID Connect scope",
            "profile": "User profile",
            "email": "User email",
        },
    }

VOUCH_URL = os.getenv('KNOT_VOUCH_URL')


# Async tasks

CELERY_BROKER_URL = 'redis://localhost'
CELERY_RESULT_BACKEND = 'redis'
CELERY_TASK_ANNOTATIONS = {'*': {'expires': 1800}}
CELERY_TASK_TIME_LIMIT = 1800
CELERY_TASK_TRACK_STARTED = True
CELERY_CONCURRENCY = 4


# Form styling with crispy-forms

CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Bootstrap compatible messages

from django.contrib.messages import constants as messages # noqa: E402

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


# File management domains

FILES_URL = os.getenv('KNOT_FILES_URL', 'file://%s' % os.path.join(BASE_DIR, 'files'))
FILES_MOUNT_DIR = os.getenv('KNOT_FILES_MOUNT_DIR', os.path.join(BASE_DIR, 'files'))


# Upload path

MEDIA_ROOT = FILES_MOUNT_DIR
CHUNKED_UPLOAD_PATH = 'uploads'


# Password file export

HTPASSWD_EXPORT_DIR = os.getenv('KNOT_HTPASSWD_EXPORT_DIR')


# Ingress domain

INGRESS_URL = os.getenv('KNOT_INGRESS_URL', 'http://localtest.me')


# Title and URLs

DASHBOARD_TITLE = os.getenv('KNOT_DASHBOARD_TITLE', 'Knot')
DOCUMENTATION_URL = os.getenv('KNOT_DOCUMENTATION_URL')
ISSUES_URL = os.getenv('KNOT_ISSUES_URL')


# Datasets

DATASETS_AVAILABLE = True if os.getenv('KNOT_DATASETS_AVAILABLE', '') else False


# Local directories allowed to be mounted in containers (in addition to file domains)

ALLOWED_HOSTPATH_DIRS = [d.strip() for d in os.getenv('KNOT_ALLOWED_HOSTPATH_DIRS', '').split(':') if d.strip()]


# Service and dataset templates

SERVICES_REPO_DIR = os.path.join(BASE_DIR, 'repo', 'services')
DATASETS_REPO_DIR = os.path.join(BASE_DIR, 'repo', 'datasets')

DISABLED_SERVICES = []
DISABLED_SERVICES_FILE = os.getenv('KNOT_DISABLED_SERVICES_FILE')
if DISABLED_SERVICES_FILE and os.path.isfile(DISABLED_SERVICES_FILE):
    with open(DISABLED_SERVICES_FILE) as f:
        DISABLED_SERVICES = [line.strip() for line in f if line.strip()]

DISABLED_DATASETS = []
DISABLED_DATASETS_FILE = os.getenv('KNOT_DISABLED_DATASETS_FILE')
if DISABLED_DATASETS_FILE and os.path.isfile(DISABLED_DATASETS_FILE):
    with open(DISABLED_DATASETS_FILE) as f:
        DISABLED_DATASETS = [line.strip() for line in f if line.strip()]


# Preconfigured service URL prefixes

import re # noqa: E402

SERVICE_URL_PREFIXES = []
SERVICE_URL_PREFIXES_FILE = os.getenv('KNOT_SERVICE_URL_PREFIXES_FILE')
if SERVICE_URL_PREFIXES_FILE and os.path.isfile(SERVICE_URL_PREFIXES_FILE):
    with open(SERVICE_URL_PREFIXES_FILE) as f:
        SERVICE_URL_PREFIXES = [line.strip() for line in f if line.strip()]

for service_url_prefix in SERVICE_URL_PREFIXES:
    if not bool(re.match(r'^[0-9a-zA-Z_\-]+$', service_url_prefix)):
        raise ValueError('Invalid characters in service URL prefix')

GENERATE_SERVICE_URLS = False if SERVICE_URL_PREFIXES else True


# JupyterHub integration

JUPYTERHUB_URL = os.getenv('KNOT_JUPYTERHUB_URL')
JUPYTERHUB_NOTEBOOK_DIR = os.getenv('KNOT_JUPYTERHUB_NOTEBOOK_DIR')


# Argo integration

ARGO_WORKFLOWS_URL = os.getenv('KNOT_ARGO_WORKFLOWS_URL')
ARGO_WORKFLOWS_NAMESPACE = os.getenv('KNOT_ARGO_WORKFLOWS_NAMESPACE')


# Harbor integration

HARBOR_URL = os.getenv('KNOT_HARBOR_URL')
HARBOR_NAMESPACE = os.getenv('KNOT_HARBOR_NAMESPACE')
HARBOR_ADMIN_PASSWORD = os.getenv('KNOT_HARBOR_ADMIN_PASSWORD')


# Grafana integration

GRAFANA_URL = os.getenv('KNOT_GRAFANA_URL')


# OpenBio integration

OPENBIO_URL = os.getenv('KNOT_OPENBIO_URL')
