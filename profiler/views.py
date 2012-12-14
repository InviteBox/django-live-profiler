from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.cache import cache
from django.contrib.auth.decorators import user_passes_test

from profiler.backends import get_backend

@user_passes_test(lambda u:u.is_superuser)
def stats(request):
    stats = get_backend().get_stats(None)
    return render_to_response('profiler/index.html',
                              {'queries' : stats},
                              context_instance=RequestContext(request))
