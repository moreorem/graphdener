# import msgpackrpc
from mprpc import RPCClient

''' This class is used to communicate with the rust backend '''
class Call():
    client = None

    @staticmethod
    def connect():
        if Call.client is None:
            Call.client = RPCClient("127.0.0.1", port=6000, timeout=3000)

    @classmethod
    def send_paths(cls, paths):
        c = cls.client
        result = c.call('import', paths)
        print(result)

    @classmethod
    def get_vert(cls, detail_type):
        c = cls.client
        print("getting vertex...")
        try:
            result = c.call('get', 'vert', detail_type)
        except e:
            result = EnvironmentError
        return result

    @classmethod
    def get_edge(cls, detail_type):
        c = cls.client
        print("getting edges...")
        result = c.call('get', 'edge', detail_type)
        return result

    # Gets positions of all of the vertices []
    @classmethod
    def get_positions(cls):
        if c is None:
            Call.connect()
        c = cls.client

        print("getting positions...")
        # Evaluate result to float list
        a = c.call('get', 'vert', 'pos')
        return result

    @classmethod
    def get_types(cls):
        c = cls.client
        print("getting types...")
        result = c.call('get_vert', [], 'type')

