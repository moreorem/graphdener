# import msgpackrpc
from mprpc import RPCClient


class Call():
    ''' This class is used to communicate with the rust backend '''
    client = None
    console = None
    graphId = 0

    @staticmethod
    def connect():
        if Call.client is None:
            Call.client = RPCClient("127.0.0.1", port=6000, timeout=3000)

    @classmethod
    def send_paths(cls, paths, regex):
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
        cls.console_out("Importing...")
        result = c.call('import', paths, regex)
        Call.console_out(result)
        cls.console_out("Ready")
        return result

    # PENDING: Replace constants with kwargs to be compatible with every algorithm
    @classmethod
    def apply_alg(cls, algorithm, *args):
        c = cls.client
        cls.console_out("Applying algorithm...")
        if algorithm == "force directed":
            parameters = [float(eval(x)) for x in args]
            c.call('diralg', cls.graphId, parameters)
        elif algorithm == "circular":
            c.call('ciralg', cls.graphId)
        elif algorithm == "random":
            parameters = int(eval(*args))
            c.call('random', cls.graphId, parameters)
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
        cls.console_out("Ready")
        return result

    @classmethod
    def populate_graph(cls):
        c = cls.client
        cls.console_out(cls.graphId, "Populating graph ")
        try:
            result = c.call('populate', cls.graphId)
            cls.console_out(result, "Populated graph ")
        except EnvironmentError as e:
            print(e)
        cls.console_out("Ready")
        return result

    @classmethod
    def get_adj(cls):
        c = cls.client
        cls.console_out("Gathering edges...")
        try:
            result = c.call('getadj', cls.graphId)
        except EnvironmentError as e:
            result = e
        cls.console_out("Ready")
        return result

    @classmethod
    def get_n_type(cls):
        c = cls.client
        cls.console_out("Gathering types...")
        try:
            result = c.call('getntype', cls.graphId)
        except EnvironmentError as e:
            result = e
        cls.console_out("Ready")
        return result

    @classmethod
    def get_n_pos(cls):
        c = cls.client
        cls.console_out("Calulating positions...")
        try:
            result = c.call('getnpos', cls.graphId)
        except EnvironmentError as e:
            result = e
        cls.console_out("Ready")
        return result

    @classmethod
    def get_stat(cls):
        c = cls.client
        try:
            result = c.call('getstat', cls.graphId)
        except EnvironmentError as e:
            result = e
        cls.console_out("Ready")
        return result

    @classmethod
    def kill_graph(cls):
        c = cls.client
        cls.console_out("Destroying graph...")
        try:
            result = c.call('killgraph', cls.graphId)
            cls.console_out(cls.graphId, "Killed graph ")
        except EnvironmentError as e:
            result = e
        cls.console_out("Ready")
        return result

    @staticmethod
    def console_out(msg, prefix=''):
        Call.console.write_out(msg)
