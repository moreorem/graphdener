import msgpackrpc

''' This class is used to communicate with the rust backend '''


class Communicator():
    client = None

    @staticmethod
    def connect():
        if Communicator.client is None:
            Communicator.client = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", port=54321))

    @classmethod
    def send_paths(cls, paths):
        c = cls.client
        result = c.call('import', paths)
        print(result)

    @classmethod
    def initialize(cls):
        c = cls.client
        print("Initializing")
        result = c.call('init', None)
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
    def get_vertex(cls, id):
        c = cls.client
        print("creating vertex...")
        if id:
            result = c.call('get_vert', id)
        else:
            result = c.call('get_vert', [])
        print(result)
