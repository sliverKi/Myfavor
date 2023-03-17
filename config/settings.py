from pathlib import Path
import os
import environ

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    #"rest_framework_simplejwt",
]

CUSTOM_APPS = [
    "users.apps.UsersConfig",
    "usersCalendar.apps.UserscalendarConfig",
    "common.apps.CommonConfig",
    "media.apps.MediaConfig",
    "idols.apps.IdolsConfig",
    "categories.apps.CategoriesConfig",
    "times.apps.TimesConfig",
]
# Application definition

SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
INSTALLED_APPS = SYSTEM_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"

MEDIA_ROOT = "uploads"
# DB저장(file이 실제로 있는 위치)
MEDIA_URL = "user-uploads/"
# upload된 파일에 접근하여 화면에 노출 시킴

# react 와 연결시켜주기위한코드
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:3000", "http://localhost:3000"]
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:3000", "http://localhost:3000"]


# SESSION_COOKIE_AGE=1200 #유지 시간 : 20분  세션 정보 갱신
# SESSION_SAVE_EVERY_REQUEST=True #사용자가 응답을 보내지 않으면 세션 타임 아웃


# GH_SECRET=env("GH_SECRET"), "insert cloudflare token"
# CF_TOKEN=env("CF_TOCKEN")
# CF_ID=env("CF_ID")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        # "config.authentication.TrustMeBrokerAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "config.authentication.JWTAuthentication",
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
    ]
}



ACCOUNT_AUTHENTICATION_METHOD = "email"  # 로그인시 username 이 아니라 email을 사용하게 하는 설정
ACCOUNT_EMAIL_REQUIRED = True  # 회원가입시 필수 이메일을 필수항목으로 만들기
ACCOUNT_USERNAME_REQUIRED = False  # USERNAME 을 필수항목에서 제거

ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = True # 비밀번호 지워지지않음
ACCOUNT_SESSION_REMEMBER = True  # 브라우저를 닫아도 세션기록 유지! [ 로그인 안풀리게 ! ]
SESSION_COOKIE_AGE = 3600