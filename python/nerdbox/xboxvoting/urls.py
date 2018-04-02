"""
URL definitions for XBox voting app

Author: Nick Stevens <nickastevens@yahoo.com>
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('xboxvoting.views',
    url(r'^$', 'index'),
    url(r'^(?P<game_id>\d+)/vote/$', 'vote'),
    url(r'^add/$', 'add'),
    url(r'^(?P<game_id>\d+)/own/$', 'own'),
    url(r'^manage.html?$', 'manage'),
    url(r'^clear_cookie.html?$', 'clear_cookie'),
)
