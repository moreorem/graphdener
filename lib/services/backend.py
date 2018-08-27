from PyQt5.QtCore import QProcess
from . import config
BPATH = config.get_directory('backend')


class Backend(object):
    proc = None
    parent = None

    def start():
        Backend.proc = QProcess()
        Backend.proc.start(BPATH + "graphdener-backend")
        # Wait for server to start and then connect
        if Backend.proc.waitForStarted(msecs=3000):
            print("Backend Connected")
            print('{}'.format(Backend.proc.pid()))

    def stop():
        if Backend.proc is not None:
            try:
                Backend.proc.close()
                # print('{}'.format(Backend.proc.pid)))
            except AttributeError as e:
                print('Unable to stop server ', e)

    # PENDING: Deprecated
    # def make_edges(lst, max_iter):
    #     ed = ([], [])

    #     for j in range(2):
    #         temp_lst = lst[:]
    #         i = 1
    #         while len(temp_lst) > 0 and i < max_iter:
    #             idx = random.randrange(0, len(temp_lst))
    #             i += 1
    #             if random.getrandbits(1) == 1:
    #                 ed[j].append(temp_lst.pop(idx))
    #             else:
    #                 ed[j].append(temp_lst[idx])

    #     return zip(ed[0], ed[1])
