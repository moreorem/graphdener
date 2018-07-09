import msgpackrpc

''' This class is used to communicate with the rust backend '''


class Communicator:
    def connect():
        client = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", port=54321))
        return client

    def send_paths(path):
        handle = Communicator.connect()
        result = handle.call('import', path)
        print(result)
