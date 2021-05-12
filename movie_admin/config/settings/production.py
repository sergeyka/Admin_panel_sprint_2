"""Production configuration"""
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': getenv('DB_NAME', 'movies'),
        'USER': getenv('DB_USER', 'movies'),
        'PASSWORD': getenv('DB_PASSWORD', 'movies'),
        'HOST': getenv('DB_HOST', '127.0.0.1'),
        'PORT': getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'options': getenv('DB_OPTIONS', '-c search_path=public,content'),
        }
    }
}
