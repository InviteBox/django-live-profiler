import threading
import hashlib

import pymongo

from django.core.cache import cache

_hash = lambda x : hashlib.md5(x).hexdigest()


class CacheBackend(object):
    
    def __init__(self, sessions):
        self.sessions = sessions

    def start_request(self):
        pass

    def end_request(self):
        pass
    
    def log_query(self, query, time):
        key = 'profiler_query_%s'%_hash(query)
        query_info = cache.get(key) 
        if query_info is None:
            query_info = { 'times_ran' : 0, 'total_time' : 0, 'query' : query}
            qlist = cache.get('profiler_query_list') or []
            qlist.append(key)
            cache.set('profiler_query_list', qlist)
        query_info['times_ran'] += 1
        query_info['total_time'] += time
        cache.set(key, query_info)
    
    def get_stats(self, session):
        qlist = cache.get('profiler_query_list') or []
        stats = []
        for q in qlist:  
            qdata = cache.get(q) 
            if qdata is None:
                continue
            st = {}
            st.update(qdata)
            st['average_time'] = st['total_time'] / st['times_ran']
            stats += [st]
        return stats
        
connection = pymongo.Connection()
queries = connection['profiler']['queries']

class MongoBackend(object):
    def __init__(self, sessions):
        self.sessions = sessions
        self.view = None

    def start_request(self):
        pass

    def end_request(self):
        pass

    def start_view(self, view):
        self.view = view

    
    def log_query(self, query, time):
        queries.insert({'query' : query,
                        'time' : time,
                        'view' : self.view,
                        'sessions' : self.sessions})
    
    def get_stats(self, session, group_by_view=False):
        if group_by_view:
            group = {'query':2, 'view' : 1}
        else:
            group = {'query':1}
        ret = queries.group(key=group, condition={}, initial={'total_time':0, 'times_ran' : 0}, reduce = 'function(obj, prev){prev.total_time += + obj.time;prev.times_ran +=1;}')
        for r in ret:
            r['average_time'] = r['total_time'] / r['times_ran']
        return ret

    def reset(self):
        queries.remove({})




_local = threading.local()

def make_backend(sessions):
    _local.backend = MongoBackend(sessions)
    return _local.backend

def get_backend():
    backend = getattr(_local, 'backend', None)
    return backend
