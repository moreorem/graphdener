# import msgpackrpc
from mprpc import RPCClient


class Call():
    ''' This class is used to communicate with the rust backend '''
    client = None

    @staticmethod
    def connect():
        if Call.client is None:
            Call.client = RPCClient("127.0.0.1", port=6000, timeout=3000)

    @classmethod
    def send_paths(cls, paths, regex, colNames):
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
        # col = [(k, v) for k, v in colNames.items()]
        c = cls.client
        result = c.call('import', paths, regex, colNames)
        return result

    # PENDING: Replace constants with kwargs to be compatible with every algorithm
    @classmethod
    def apply_alg(cls, graphId, algorithm, *args):
        c = cls.client
        if algorithm == "force directed":
            parameters = [float(eval(x)) for x in args]
            c.call('diralg', graphId, parameters)
        elif algorithm == "circular":
            c.call('ciralg', graphId)
        elif algorithm == "random":
            parameters = int(eval(*args))
            c.call('random', graphId, parameters)

    @classmethod
    def create_graph(cls):
        c = cls.client
        print("Creating graph...")
        try:
            result = c.call('newgraph')
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

    # NEW ORIGIN
    @classmethod
    def get_adj(cls, canvas_id):
        c = cls.client
        print("getting edges...")
        try:
            result = c.call('getadj', canvas_id)
        except EnvironmentError as e:
            result = e
        return result

    @classmethod
    def get_n_type(cls, canvas_id):
        c = cls.client
        print("getting node types...")
        try:
            result = c.call('getntype', canvas_id)
        except EnvironmentError as e:
            result = e
        return result

    # NEW ORIGIN
    @classmethod
    def get_n_pos(cls, canvas_id):
        c = cls.client
        print("getting vertex positions...")
        try:
            result = c.call('getnpos', canvas_id)
        except EnvironmentError as e:
            result = e
        return result

    @classmethod
    def get_stat(cls, canvas_id):
        c = cls.client
        print("getting stats...")
        try:
            result = c.call('getstat')
        except EnvironmentError as e:
            result = e
        return result


