"""
Django settings for recipes project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')^1t4$hc8yw$i=l1=da%urz*u4=y-^)%$g8*#9dbn5@mb$s&k3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = 'test@gmail.com'
    SERVER_EMAIL = 'test@gmail.com'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'test@gmail.com'
    EMAIL_HOST_PASSWORD = 'test123##'
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = ('/home/saloni/recipes/template',)

LOGIN_URL = '/recipes/login/'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allrecipes',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'recipes.urls'

WSGI_APPLICATION = 'recipes.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'recipes',
        'USER':'root',
        'PASSWORD':'saloni11',
        'HOST':'localhost',
        'PORT':'',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/home/saloni/recipes/allrecipes/static/'

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__).decode('utf-8'))

MEDIA_ROOT = '/home/saloni/recipes/allrecipes/images/media/'
MEDIA_URL = '/media/'
