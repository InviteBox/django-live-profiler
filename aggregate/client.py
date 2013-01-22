import threading

import zmq 

class _RemoteMethod:
    def __init__(self, socket, name):
        self.socket = socket
        self.name = name

    def __call__(self, *args, **kwargs):
        self.socket.send_pyobj((self.name, args, kwargs))
        return self.socket.recv_pyobj()

class Aggregator(object):
    def __init__(self):
        self.context = zmq.Context()
        self.data_socket = self.context.socket(zmq.PUB)
        self.data_socket.connect ("tcp://localhost:5556")
        self.control_socket = self.context.socket(zmq.REQ)
        self.control_socket.connect("tcp://localhost:5557")
    
    def insert(self, tags, values):
        self.insert_all([(tags, values)])
        
    def insert_all(self, items):
        self.data_socket.send_pyobj(items)
        
        
    def __getattr__(self, name):
        return _RemoteMethod(self.control_socket, name)
    
    def ping(self):
        self.data_socket.send_pyobj(None)


_local = threading.local()

def get_client():
    try:
        return _local.aggregator
    except AttributeError:
        _local.aggregator = Aggregator()
        return _local.aggregator
