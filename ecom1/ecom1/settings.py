
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Define your templates directory
TEMP_DIR = BASE_DIR / 'templates'



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&$bxfg9s3re0gf4q+&!ee1=x4i)!g$t9435nk3l&sat-(jxu80'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'account',
    'admin_panel',
    'payment'
 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecom1.urls'

import os

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # This line should use the Path object
            BASE_DIR / 'ecom1' / 'admin_panel' / 'templates',  # Similarly, use Path for the admin panel template
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',

            ],
        },
    },
]



WSGI_APPLICATION = 'ecom1.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'fathimathusana51@gmail.com'  # Replace with your email address
EMAIL_HOST_PASSWORD = 'ezqu fofo gndo iahe'


AUTH_USER_MODEL = 'admin_panel.CustomUser'

STRIPE_PUBLISHABLE_KEY ="pk_test_51QcQ0PFHIp6m4TV9reTKml3UP6MAECkwJP5sTw87vLFgnHtjbkSthuxWAxhdBL6ZLQjwlFlkrrR8gdUKMULFaNUc00BBimqbAT"
STRIPE_SECRET_KEY = "sk_test_51QcQ0PFHIp6m4TV9z4ObwmtvvrTl5B8PXsLP9NnO0Eh1GaoTQ8AGMuruYzM6z7dnP0ZEKhdbdrHo9iMpaW1AxDsV00A7Oh94kl"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'project1',
        'USER': 'postgres',
        'PASSWORD': 'sana123',
        'HOST': 'localhost',  # or the IP address of the database server
        'PORT': '5432',       # default PostgreSQL port
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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

LOGIN_URL = 'login_view'


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
