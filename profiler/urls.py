from django.conf.urls.defaults import *

urlpatterns = patterns(
    'profiler.views',
    url(r'^$', 'global_stats', name='profiler_global_stats'),
    url(r'^by_view/$', 'stats_by_view', name='profiler_stats_by_view'),
    )

