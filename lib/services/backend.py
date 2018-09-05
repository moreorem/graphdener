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

