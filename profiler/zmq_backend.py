import zmq
import random

from profiler.aggregator import Aggregator


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


def ctl(aggregator):
    context = zmq.Context.instance()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5557")
    while True:
        cmd, args, kwargs = socket.recv_pyobj()
        if cmd == 'get_stats':
            if kwargs['group_by_view']:
                ret = aggregator.select(group_by=['view', 'query'])
            else:
                ret = aggregator.select(group_by=['query'])
            for v in ret:
                v['average_time'] = v['total_time'] / v['times_ran']
            socket.send_pyobj(ret)
        elif cmd == 'reset':
            aggregator.clear()
            socket.send_pyobj(True)

if __name__ == "__main__":
    context = zmq.Context.instance()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://*:5556")
    socket.setsockopt(zmq.SUBSCRIBE,'')
    a = Aggregator()
    statthread = Thread(target=ctl, args=(a,))
    statthread.start()
        
    while True:
        q = socket.recv_pyobj()
        a.insert({'query' : q['query'],
                  'view' : q['view']},
                 {'total_time' : q['time'],
                  'times_ran' : 1})
