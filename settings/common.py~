"""
Django settings for proyecto_colima project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v50#tsbp-13tdxb54=9e-n=oqby&-808bo1z=ezc2a()rpczv%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['locahost']

#Rutas de nuestros templates
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'proyecto_colima/templates', ''),
    os.path.join(BASE_DIR, 'inicio/templates', ''),
)

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    # "django.core.context_processors.debug",
    # "django.core.context_processors.i18n",
    # "django.core.context_processors.media",
    # "django.core.context_processors.static",
    # 'django.core.context_processors.request',
)



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inicio',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'proyecto_colima.urls'

WSGI_APPLICATION = 'proyecto_colima.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases



# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'inicio/static', ''),
)


TIEMPO_EXPIRACION_SESION = 14400


#Repositorio de archivos
REPOSITORIO_GENERAL             = os.path.join(BASE_DIR, 'repositorio', '') 

PERSONAL                        = os.path.join(REPOSITORIO_GENERAL, 'personal', '')
DETALLES_PAGO_EMPLEADO          = os.path.join(REPOSITORIO_GENERAL, 'detalles_pago_empleado', '')
DETALLES_DOCUMENTO_RESPONSIVA   = os.path.join(REPOSITORIO_GENERAL, 'detalles_documento_responsiva', '')
ANEXOS_TECNICOS                 = os.path.join(REPOSITORIO_GENERAL, 'anexos_tecnicos', '')
CONVENIOS                       = os.path.join(REPOSITORIO_GENERAL, 'convenios', '')
CONTRATOS                       = os.path.join(REPOSITORIO_GENERAL, 'contratos', '')
ENTREGABLES                     = os.path.join(REPOSITORIO_GENERAL, 'entregables', '')
DETALLES_ENTREGABLES            = os.path.join(REPOSITORIO_GENERAL, 'detalles_entregables', '')
FACTURAS                        = os.path.join(REPOSITORIO_GENERAL, 'facturas', '')
DETALLE_DOCUMENTOS_GENERALES    = os.path.join(REPOSITORIO_GENERAL, 'detalle_documentos_generales', '')