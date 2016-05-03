from .base import *

DEBUG = True

INSTALLED_APPS.append(
    'debug_toolbar'
)

MIDDLEWARE_CLASSES.append(
    'debug_toolbar.middleware.DebugToolbarMiddleware'
)
