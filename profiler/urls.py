from django.conf.urls.defaults import *

urlpatterns = patterns(
    'profiler.views',
    url(r'^$', 'stats', name='profiler_stats'),
    )

