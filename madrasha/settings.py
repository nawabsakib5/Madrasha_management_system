import environ
from pathlib import Path

# ─── Base Directory ───────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Environment Variables ────────────────────────────────
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

# ─── Security ─────────────────────────────────────────────
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost'])

# ─── Multi-Tenancy (django-tenants) ───────────────────────
SHARED_APPS = [
    'django_tenants',
    'apps.saas',
    'apps.accounts',

    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
]

TENANT_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',

    'apps.accounts',
    'apps.core',
    'apps.students',
    'apps.academics',
    'apps.staff',
    'apps.accounting',
    'apps.donation',
    'apps.library',
    'apps.attendance',
    'apps.examination',
    'apps.canteen',
    'apps.branch',
    'apps.portal',
]

INSTALLED_APPS = list(SHARED_APPS) + [
    app for app in TENANT_APPS
    if app not in SHARED_APPS
]

TENANT_MODEL = 'saas.Tenant'
TENANT_DOMAIN_MODEL = 'saas.Domain'

# ─── Middleware ───────────────────────────────────────────
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',  # must be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ─── URLs ─────────────────────────────────────────────────
ROOT_URLCONF = 'madrasha.urls'
PUBLIC_SCHEMA_URLCONF = 'madrasha.urls'

# ─── Templates ────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'madrasha.wsgi.application'

# ─── Database (PostgreSQL) ────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

DATABASE_ROUTERS = ['django_tenants.routers.TenantSyncRouter']

# ─── Password Validation ──────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Internationalization ─────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True

# ─── Static & Media Files ─────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─── Default Primary Key ──────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── Custom User Model ────────────────────────────────────
AUTH_USER_MODEL = 'accounts.User'

# ─── Redis & Celery ───────────────────────────────────────
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')

# ─── Email ────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# ─── Session Timeout (30 minutes) ────────────────────────
SESSION_COOKIE_AGE = 1800
SESSION_SAVE_EVERY_REQUEST = True