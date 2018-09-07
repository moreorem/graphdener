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
    def get_vert(cls, detail_type, canvas_id):
        c = cls.client
        print("getting vertex...")
        try:
            result = c.call('get', 'vert', detail_type, canvas_id)
        except EnvironmentError as e:
            result = e
        return result

    @classmethod
    def get_edge(cls, detail_type, canvas_id):
        c = cls.client
        print("getting edges...")
        try:
            result = c.call('get', 'edge', detail_type, canvas_id)
        except EnvironmentError as e:
            result = e
        return result

