import msgpackrpc

''' This class is used to communicate with the rust backend '''
class Call():
    client = None

    @staticmethod
    def connect():
        if Call.client is None:
            Call.client = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", port=54321))

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
    def get_vertex(cls, id, detail_type):
        c = cls.client
        print("creating vertex...")
        if id:
            result = c.call('get_vert', id, detail_type)
        else:
            result = c.call('get_vert', [], detail_type)
        print(result)

    # Gets positions of all of the vertices []
    @classmethod
    def get_positions(cls):
        c = cls.client
        print("creating vertex...")
        result = c.call('get_vert', [], 'pos')

        print(result)
