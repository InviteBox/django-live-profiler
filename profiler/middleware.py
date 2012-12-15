from datetime import datetime

from django.db import connection
from django.core.cache import cache

from profiler import backends

class ProfilerMiddleware(object):

    def process_request(self, request):
        active_sessions = cache.get('profiler_active_sessions', [])
        #TODO: filter sessions by condition
        backend = backends.make_backend(active_sessions)
        backend.start_request()
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        backend = backends.get_backend()
        backend.start_view(str(view_func))
        return None
    
    def process_response(self, request, response):
        backend = backends.get_backend()
        backend.end_request()
        return response


