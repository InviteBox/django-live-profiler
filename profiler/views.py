from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.cache import cache
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.utils import simplejson

from aggregate.client import get_client

@user_passes_test(lambda u:u.is_superuser)
def global_stats(request):
    stats = get_client().select(group_by=['query'], where={'type':'sql'})
    for s in stats:
        s['average_time'] = s['time'] / s['count']
    return render_to_response('profiler/index.html',
                              {'queries' : stats},
                              context_instance=RequestContext(request))

@user_passes_test(lambda u:u.is_superuser)
def stats_by_view(request):
    stats = get_client().select(group_by=['view','query'], where={'type':'sql'})
    grouped = {}
    for r in stats:
        if r['view'] not in grouped:
            grouped[r['view']] = {'queries' : [], 
                                  'count' : 0,
                                  'time' : 0,
                                  'average_time' : 0}
        grouped[r['view']]['queries'].append(r)
        grouped[r['view']]['count'] += r['count']
        grouped[r['view']]['time'] += r['time']
        r['average_time'] = r['time'] / r['count'] 
        grouped[r['view']]['average_time'] += r['average_time']
        
    maxtime = 0
    for r in stats:
        if r['average_time'] > maxtime:
            maxtime = r['average_time']
    for r in stats:
        r['normtime'] = (0.0+r['average_time'])/maxtime
           
    return render_to_response('profiler/by_view.html',
                              {'queries' : grouped,
                               'stats' :simplejson.dumps(stats)},
                              context_instance=RequestContext(request))

@user_passes_test(lambda u:u.is_superuser)
def reset(request):
    next = request.GET.get('next') or request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('profiler_global_stats')
    if request.method == 'POST':
        get_client().clear()
        return HttpResponseRedirect(next)
    return render_to_response('profiler/reset.html',
                              {'next' : next},
                              context_instance=RequestContext(request))



@user_passes_test(lambda u:u.is_superuser)
def python_stats(request):
    stats = get_client().select(group_by=['file','lineno'], where={'type':'python'})
    return render_to_response('profiler/code.html',
                              {'stats' : stats},
                              context_instance=RequestContext(request))
