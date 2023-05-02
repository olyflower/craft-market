import os

from config.settings.base import *  # noqa

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["localhost"]

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

STATIC_ROOT = BASE_DIR / "static_content/"
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media_content/"
MEDIA_URL = "/media/"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
