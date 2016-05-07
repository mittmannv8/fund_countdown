from django.conf.urls import url

from fundcountdown.core.views import home


urlpatterns = [
    url(r'^$', home, name='home'),
]
