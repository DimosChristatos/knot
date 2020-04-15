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
Django settings for karvdash project.

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


# Application definition

INSTALLED_APPS = [
    'dashboard.apps.DashboardConfig',
    'crispy_forms',
    'impersonate',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
]

ROOT_URLCONF = 'karvdash.urls'

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

WSGI_APPLICATION = 'karvdash.wsgi.application'


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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.getenv('KARVDASH_DATABASE_DIR', BASE_DIR), 'db.sqlite3'),
    }
}


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


# Authentication

AUTHENTICATION_BACKENDS = ['dashboard.auth_backends.ProxiedModelBackend']
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


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


# Data management domains

# local_name = os.getenv('KARVDASH_LOCAL_NAME', 'local')
# remote_name = os.getenv('KARVDASH_REMOTE_NAME', 'remote')
# shared_name = os.getenv('KARVDASH_SHARED_NAME', 'shared')
local_name = 'local'
remote_name = 'remote'
shared_name = 'shared'

DATA_DOMAINS = {}
if local_name:
    local_default_dir = os.path.join(BASE_DIR, local_name)
    DATA_DOMAINS[local_name] = {'dir': os.getenv('KARVDASH_LOCAL_DIR', local_default_dir),
                                'host_dir': os.getenv('KARVDASH_LOCAL_HOST_DIR', local_default_dir)}
if remote_name:
    remote_default_dir = os.path.join(BASE_DIR, remote_name)
    DATA_DOMAINS[remote_name] = {'dir': os.getenv('KARVDASH_REMOTE_DIR', remote_default_dir),
                                 'host_dir': os.getenv('KARVDASH_REMOTE_HOST_DIR', remote_default_dir)}
if shared_name:
    shared_default_dir = os.path.join(BASE_DIR, shared_name)
    DATA_DOMAINS[shared_name] = {'dir': os.getenv('KARVDASH_SHARED_DIR', shared_default_dir),
                                 'host_dir': os.getenv('KARVDASH_SHARED_HOST_DIR', shared_default_dir),
                                 'mode': 'shared'}


# Docker registry endpoint

DOCKER_REGISTRY = os.getenv('KARVDASH_DOCKER_REGISTRY', 'http://127.0.0.1:5000')


# Service templates

SERVICE_TEMPLATE_DIR = os.getenv('KARVDASH_SERVICE_TEMPLATE_DIR', os.path.join(BASE_DIR, 'services'))
SERVICE_DATABASE_DIR = os.getenv('KARVDASH_SERVICE_DATABASE_DIR', os.path.join(BASE_DIR, 'servicedb'))
SERVICE_REDIRECT_SSL = True if os.getenv('KARVDASH_SERVICE_REDIRECT_SSL', '') else False


# API URL

API_BASE_URL = os.getenv('KARVDASH_API_BASE_URL')


# Ingress domain

INGRESS_DOMAIN = os.getenv('KARVDASH_INGRESS_DOMAIN', 'localtest.me')


# Theme

DASHBOARD_TITLE = os.getenv('KARVDASH_DASHBOARD_TITLE', 'Dashboard')
DASHBOARD_THEME = os.getenv('KARVDASH_DASHBOARD_THEME', 'evolve')
