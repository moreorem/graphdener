# import msgpackrpc
from mprpc import RPCClient


class Call():
    ''' This class is used to communicate with the rust backend '''
    client = None
    console = None

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
        Call.console_out(result)

    # PENDING: Replace constants with kwargs to be compatible with every algorithm
    @classmethod
    def apply_alg(cls, graphId, algorithm, *args):
        c = cls.client
        cls.console_out("Applying algorithm...")
        if algorithm == "force directed":
            parameters = [float(eval(x)) for x in args]
            c.call('diralg', graphId, parameters)
        elif algorithm == "circular":
            c.call('ciralg', graphId)
        elif algorithm == "random":
            parameters = int(eval(*args))
            c.call('random', graphId, parameters)
        cls.console_out("Ready")

    @classmethod
    def create_graph(cls):
        c = cls.client
        msg = "Creating graph..."
        cls.console_out(msg)
        try:
            result = c.call('newgraph')
            cls.console_out(result, "Created graph with id: ")
        except EnvironmentError as e:
            print(e)
        return result

    @classmethod
    def populate_graph(cls, id):
        c = cls.client
        cls.console_out(id, "Populating graph ")
        try:
            result = c.call('populate', id)
            cls.console_out(result, "Populated graph ")
        except EnvironmentError as e:
            print(e)
        return result

    @classmethod
    def get_adj(cls, canvas_id):
        c = cls.client
        cls.console_out("Gathering edges...")
        try:
            result = c.call('getadj', canvas_id)
        except EnvironmentError as e:
            result = e
        return result

    @classmethod
    def get_n_type(cls, canvas_id):
        c = cls.client
        cls.console_out("Gathering types...")
        try:
            result = c.call('getntype', canvas_id)
        except EnvironmentError as e:
            result = e
        return result

    @classmethod
    def get_n_pos(cls, canvas_id):
        c = cls.client
        cls.console_out("Calulating positions...")
        try:
            result = c.call('getnpos', canvas_id)
        except EnvironmentError as e:
            result = e
        return result

    @classmethod
    def get_stat(cls, canvas_id):
        c = cls.client
        try:
            result = c.call('getstat')
        except EnvironmentError as e:
            result = e
        return result

    @classmethod
    def kill_graph(cls, canvas_id):
        c = cls.client
        cls.console_out("Destroying graph...")
        try:
            result = c.call('killgraph', canvas_id)
            cls.console_out(canvas_id, "Killed graph ")
        except EnvironmentError as e:
            result = e
        return result

    @staticmethod
    def console_out(msg, prefix=''):
        Call.console.write_out(msg)
        print(msg)
