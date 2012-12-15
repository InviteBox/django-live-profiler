from datetime import datetime
import inspect

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
        if inspect.ismethod(view_func):
            view_name = view_func.im_class.__module__+ '.' + view_func.im_class.__name__ + view_func.__name__
        else:
            view_name = view_func.__module__ + '.' + view_func.__name__
        backend = backends.get_backend()        
        backend.start_view(view_name)
        return None
    
    def process_response(self, request, response):
        backend = backends.get_backend()
        backend.end_request()
        return response


