from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'so_factory',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '192.168.100.2',
        'PORT': '3306',
        'OPTIONS': {
        'init_command': 'SET storage_engine=INNODB',
        },
    }
}

print DATABASES