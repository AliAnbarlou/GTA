from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-fwq=5gp@0t7b3@gqctm7luf*(2+el-sut6et3z-rc-w9t*#m7y'

DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',

    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Admin',
    'Donate',
    'Authentication',
    'Home',
    'Word',
    'Translate',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Home.Middleware.SaveIPMiddleware',#Home
]

ROOT_URLCONF = 'Zabanzad.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'Templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Home.context_processors.account_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'Zabanzad.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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

LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'Authentication.User'

SITE_NAME = "Zabanzad"

# statics
STATIC_URL = '/Static/'
STATICFILES_DIRS = [BASE_DIR / "Static"]

# medias
MEDIA_URL = '/Media/'
MEDIA_ROOT = BASE_DIR / 'Media'  # باید از / به جای کاما استفاده کنید


LOGOUT_REDIRECT_URL = '/'  # یا هر صفحه‌ای که می‌خواهید بعد از خروج بروید

LOGIN_REDIRECT_URL = 'Authentication:UserHome'
LOGIN_URL = 'Authentication:login'

"""
# جلوگیری از ایندکس شدن صفحات
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'  # جلوگیری از بارگذاری صفحه در iframe
SECURE_SSL_REDIRECT = True  # اجباری کردن HTTPS
SESSION_COOKIE_SECURE = True  # فقط ارسال کوکی‌های جلسه از طریق HTTPS
CSRF_COOKIE_SECURE = True  # فقط ارسال کوکی CSRF از طریق HTTPS
SECURE_HSTS_SECONDS = 3600  # فعال کردن HSTS
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # شامل زیر دامنه‌ها در HSTS
SECURE_HSTS_PRELOAD = True  # اجازه به مرورگرها برای پیش‌بارگذاری HSTS

"""
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # احراز هویت پیش‌فرض
]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
from django.urls import reverse_lazy

PASSWORD_CHANGE_REDIRECT_URL = reverse_lazy('Authentication:password_change_done')
