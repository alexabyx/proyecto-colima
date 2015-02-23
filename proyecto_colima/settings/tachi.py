from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'so_factory',
        'USER': 'user',
        'PASSWORD': 'contrasenya',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
        'init_command': 'SET storage_engine=INNODB',
        },
    }
}
