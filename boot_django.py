# File sets up the django environment, used by other scripts that need to
# execute in django land
import os
import django
from django.conf import settings

APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'saasbase'))

def boot_django():
    settings.configure(
        BASE_DIR=APP_DIR,
        DEBUG=True,
        DATABASES={
            'default':{
                'ENGINE':'django.db.backends.sqlite3',
                'NAME': os.path.join(APP_DIR, 'db.sqlite3'),
            }
        },
        ROOT_URLCONF='saasbase.tests.urls',
        MIDDLEWARE = (
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.admin',

            'awl',
            'localflavor',

            'saasbase',
        ),
        #TEMPLATES = [{
        #    'BACKEND':'django.template.backends.django.DjangoTemplates',
        #    'DIRS':[
        #        os.path.abspath(os.path.join(APP_DIR, 'tests/data/templates')),
        #    ],
        #    'APP_DIRS':True,
        #    'OPTIONS': {
        #        'context_processors':[
        #            'django.template.context_processors.debug',
        #            'django.template.context_processors.request',
        #            'django.contrib.auth.context_processors.auth',
        #            'django.contrib.messages.context_processors.messages',
        #        ]
        #    }
        #}],
        #WRUNNER = {
        #    'CREATE_TEMP_MEDIA_ROOT':True,
        #},
    )
    django.setup()
