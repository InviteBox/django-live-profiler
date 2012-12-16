from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.cache import cache
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse

from profiler.backends import get_backend

@user_passes_test(lambda u:u.is_superuser)
def global_stats(request):
    stats = get_backend().get_stats(None)
    return render_to_response('profiler/index.html',
                              {'queries' : stats},
                              context_instance=RequestContext(request))

@user_passes_test(lambda u:u.is_superuser)
def stats_by_view(request):
    stats = get_backend().get_stats(None, group_by_view=True)
    grouped = {}
    for r in stats:
        if r['view'] not in grouped:
            grouped[r['view']] = {'queries' : [], 
                                  'times_ran' : 0,
                                  'total_time' : 0,
                                  'average_time' : 0}
        grouped[r['view']]['queries'].append(r)
        grouped[r['view']]['times_ran'] += r['times_ran']
        grouped[r['view']]['total_time'] += r['total_time']
        grouped[r['view']]['average_time'] += r['average_time']
        
        
    return render_to_response('profiler/by_view.html',
                              {'queries' : grouped},
                              context_instance=RequestContext(request))

@user_passes_test(lambda u:u.is_superuser)
def reset(request):
    next = request.GET.get('next') or request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('profiler_global_stats')
    if request.method == 'POST':
        get_backend().reset()
        return HttpResponseRedirect(next)
    return render_to_response('profiler/reset.html',
                              {'next' : next},
                              context_instance=RequestContext(request))
