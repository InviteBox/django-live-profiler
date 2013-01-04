import threading

_local = threading.local()

def _set_current_view(view):
    _local.current_view = view

def _get_current_view():
    return getattr(_local, 'current_view', None)
