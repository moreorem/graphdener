# import msgpackrpc
from mprpc import RPCClient

''' This class is used to communicate with the rust backend '''
class Call():
    client = None

    @staticmethod
    def connect():
        if Call.client is None:
            Call.client = RPCClient("127.0.0.1", port=54321)

    @classmethod
    def send_paths(cls, paths):
        c = cls.client
        result = c.call('import', paths)
        print(result)

    @classmethod
    def create_vertex(cls, vertexType):
        c = cls.client
        print("creating vertex...")
        result = c.call('c_vert', vertexType)
        print(result)

    @classmethod
    def create_edge(cls):
        c = cls.client
        print("creating vertex...")
        result = c.call('c_edge', None)
        print(result)

    @classmethod
    def get_vertex(cls, id, detail_type):
        c = cls.client
        print("creating vertex...")
        if id:
            result = c.call('get', 'vert', id, detail_type)
        else:
            result = c.call('get', 'vert', detail_type)
        print(result)

    @classmethod
    def get_edge(cls, detail_type):
        c = cls.client
        print("getting edges...")
        result = c.call('get', 'edge', detail_type)
        print(result)

    # Gets positions of all of the vertices []
    @classmethod
    def get_positions(cls):
        c = cls.client
        print("getting positions...")
        # Evaluate result to float list
        result = [eval(x) for x in c.call('get_vert', [], 'pos')]
        return result

    @classmethod
    def get_types(cls):
        c = cls.client
        print("getting types...")
        result = c.call('get_vert', [], 'type')

        print(result)
