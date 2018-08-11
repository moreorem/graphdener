from indradb import *
from PyQt5.QtCore import QProcess
import random
from . import backend

# static class for database communication (indradb)


class Database(object):
    proc = None
    client = None
    nodesID = '00000000-0000-0000-0000-000000000000'
    dbPath = '/home/orestes/Workspace/github.com/moreorem/graphdener-backend/target/debug/graphdener-backend'
    parent = None
    adj = None

    @staticmethod
    def start_server(self):
        Database.proc = QProcess(Database.parent)
        Database.proc.start(Database.dbPath + "indradb")
        # Wait for server to start and then connect
        if Database.proc.waitForStarted(msecs=3000):
            Database.client = Client('0.0.0.0:8000', request_timeout=60, scheme='http')
            print("Database Connected")

    def stop_server():
        if Database.proc is not None:
            try:
                Database.proc.terminate()
                Database.proc = None
                print('Server stopped')
            except AttributeError as e:
                print('Unable to stop server ', e)

    @staticmethod
    def import_data(self):
        trans = Transaction()


    def create_random_dataset(self):
        trans = Transaction()
        for i in range(10):
            trans.create_vertex_from_type('person')
        vertices = Database.client.transaction(trans)

        # Create random edges
        ed = Database.make_edges(vertices, 10)
        ed = list(ed)

        # List of dict that contains edgekeys
        edgeDict = [{"outbound_id": ed[0], "type": "relation", "inbound_id": ed[1]} for i in ed]

        trans = Transaction()
        # print('the key of this edge is: {}'.format(ek.to_dict()))
        # for i in range(len())
        for i in range(len(edgeDict)):
            ek = EdgeKey.from_dict(edgeDict[0])
            print(ek)
            trans.create_edge(ek)
        # dd = Database.client.transaction(trans)
        # print(dd)
        return

    def make_edges(lst, max_iter):
        ed = ([], [])

        for j in range(2):
            temp_lst = lst[:]
            i = 1
            while len(temp_lst) > 0 and i < max_iter:
                idx = random.randrange(0, len(temp_lst))
                i += 1
                if random.getrandbits(1) == 1:
                    ed[j].append(temp_lst.pop(idx))
                else:
                    ed[j].append(temp_lst[idx])

        return zip(ed[0], ed[1])

    @staticmethod
    def list_all_vertices(self):
        # trans = Transaction()
        vertices = backend.Communicator.get_vertex(None)
        Database.nodesID = tuple(x.id for x in vertices)
        print(Database.nodesID)

    def list_all_edges():
        trans = Transaction()
        # ed = trans.get_edges(get_vertices(VertexQuery.all(None, 1000)).outbound_edges(100))
        ed = trans.get_edges(EdgeQuery(VertexQuery.all(None, 100)))
        print(ed)
        print(Database.client.transaction(trans))
        # print([x.key for x in Database.client.transaction(trans)])
