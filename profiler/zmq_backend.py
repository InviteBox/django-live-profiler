import zmq
import random



class ZmqBackend(object):
    def __init__(self, sessions):
        self.context = zmq.Context()
        self.log_socket = self.context.socket(zmq.PUB)
        self.log_socket.connect ("tcp://localhost:5556")
        self.control_socket = self.context.socket(zmq.REQ)
        self.control_socket.connect("tcp://localhost:5557")
        self.view = None
        self.sessions = sessions
    
    def start_request(self):
        pass

    def end_request(self):
        pass

    def start_view(self, view):
        self.view = view

    
    def log_query(self, query, time):
        self.log_socket.send_pyobj({'query' : query,
                                    'time' : time,
                                    'view' : self.view,
                                    'sessions' : self.sessions})
    
    def get_stats(self, session, group_by_view=False):
        self.control_socket.send_pyobj(('get_stats', [], {'group_by_view' : group_by_view}))
        return self.control_socket.recv_pyobj()

    def reset(self):
        self.control_socket.send_pyobj(('reset', [], {1:2}))
        return self.control_socket.recv_pyobj()
        
from threading import Thread

from zmq.eventloop import ioloop


def ctl(queries, views):
    context = zmq.Context.instance()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5557")
    while True:
        cmd, args, kwargs = socket.recv_pyobj()
        if cmd == 'get_stats':
            if kwargs['group_by_view']:
                ret = []
                for k,v in views.items():
                    for vv in v.values():
                        vv['view'] = k
                        ret.append(vv)
            else:
                ret = queries.values()
            for v in ret:
                v['average_time'] = v['total_time'] / v['times_ran']
            socket.send_pyobj(ret)
        elif cmd == 'reset':
            queries.clear()
            views.clear()
            socket.send_pyobj(True)

if __name__ == "__main__":
    context = zmq.Context.instance()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://*:5556")
    socket.setsockopt(zmq.SUBSCRIBE,'')
    queries = {}
    views = {}
    statthread = Thread(target=ctl, args=(queries, views))
    statthread.start()
    def store(q, queries):
        query = q['query']

        try:
            stored = queries[query]
        except KeyError:
            stored = queries[query] = {
                'query' : query,
                'times_ran' : 0,
                'total_time' : 0.0,
                }
        
        stored['times_ran'] += 1
        stored['total_time'] += q['time']
        
    while True:
        q = socket.recv_pyobj()
        store(q, queries)
        try:
            view_data = views[q['view']]
        except KeyError:
            view_data = views[q['view']] = {}
        store(q, view_data)
    
