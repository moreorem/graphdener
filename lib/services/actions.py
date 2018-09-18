# import msgpackrpc
from mprpc import RPCClient

''' This class is used to communicate with the rust backend '''

# TODO: Add regexp send to actions for edge import and node import
class Call():
    client = None

    @staticmethod
    def connect():
        if Call.client is None:
            Call.client = RPCClient("127.0.0.1", port=6000, timeout=3000)

    @classmethod
    def send_paths(cls, paths, regexN, regexE):
        """
        Send paths of node and edge file to be imported by the backend.

        Parameters
        ----------
        paths : array
            [Nodes path, Edge path]
        regexN : array
            regular expression of node file
        regexE : array
            regular expression of edge file

        Returns
        -------
        """
        c = cls.client
        result = c.call('import', paths, regexN, regexE)
        print(result)


    @classmethod
    def create_graph(cls, id):
        c = cls.client
        print("Creating graph {}".format(id))
        try:
            result = c.call('graph', id)
        except Error as e:
            print(e)
        return result

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

