"""
URL definitions for "nerdbox" container. Just passes everything going
to /xbox/ to the XBox voting app

Author: Nick Stevens <nickastevens@yahoo.com>
"""
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^xbox/', include('xboxvoting.urls')),
)
