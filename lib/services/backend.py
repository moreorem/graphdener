from PyQt5.QtCore import QProcess
import random
from . import actions
from . import config

BPATH = config.get_directory('backend')



class Backend(object):
    proc = None
    nodesID = '00000000-0000-0000-0000-000000000000'
    parent = None
    adj = None

    def start():
        Backend.proc = QProcess(Backend.parent)
        Backend.proc.start(BPATH + "graphdener-backend")
        # Wait for server to start and then connect
        if Backend.proc.waitForStarted(msecs=3000):
            print("Backend Connected")

    def stop():
        if Backend.proc is not None:
            try:
                Backend.proc.terminate()
                Backend.proc = None
                print('Server stopped')
            except AttributeError as e:
                print('Unable to stop server ', e)

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
