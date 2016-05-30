from .base import *

DEBUG = True

INSTALLED_APPS.append(
    'debug_toolbar'
)

MIDDLEWARE_CLASSES.append(
    'debug_toolbar.middleware.DebugToolbarMiddleware'
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "scripts/dist"),
    # os.path.join(BASE_DIR, "styles/dist"),
)
