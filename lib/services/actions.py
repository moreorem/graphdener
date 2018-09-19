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
    def send_paths(cls, paths, regexN, regexE, colN, colE):
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
        result = c.call('import', paths, regexN, regexE, colN, colE)
        print(result)

    # PENDING: Replace constants with kwargs to be compatible with every algorithm
    @classmethod
    def refresh(cls, graphId, L=None, K_r=None, K_s=None, Delta_t=None):
        """
            Refresh the force directed model

            Parameters
            ----------
            graphId : integer
                the id of graph to update
            L : float
                spring rest length
            K_r : float
                repulsive force constant
            K_s : float
                spring constant
            delta_t : float
                time step

            Returns
            -------
        """
        c = cls.client
        if algorithm is "forcedir":
            result = c.call('diralg', graphId, L, K_r, K_s, Delta_t)
        elif algorithm is "circular":
            result = c.call('ciralg', graphId)
        print(result)

    @classmethod
    def create_graph(cls, id):
        c = cls.client
        print("Creating graph {}".format(id))
        try:
            result = c.call('newgraph', id)
        except EnvironmentError as e:
            print(e)
        return result

    @classmethod
    def populate_graph(cls, id):
        c = cls.client
        print("Populating graph {}".format(id))
        try:
            result = c.call('populate', id)
        except EnvironmentError as e:
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

    @classmethod
    def update_pos(cls, canvas_id):
        c = cls.client
        print("update step...")
        try:
            result = c.call('getpos', canvas_id)
        except EnvironmentError as e:
            result = e
        return result

