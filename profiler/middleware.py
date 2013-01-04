from datetime import datetime
import inspect

#import statprof

from django.db import connection
from django.core.cache import cache


from aggregate.client import get_client

from profiler import _set_current_view

class ProfilerMiddleware(object):

    def process_request(self, request):
        client = get_client()
        
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        if inspect.ismethod(view_func):
            view_name = view_func.im_class.__module__+ '.' + view_func.im_class.__name__ + view_func.__name__
        else:
            view_name = view_func.__module__ + '.' + view_func.__name__
        
        _set_current_view(view_name)
        return None

    
    def process_response(self, request, response):
        _set_current_view(None)
        #statprof.stop()
        return response


