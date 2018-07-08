import msgpackrpc


''' This class is used to communicate with the rust backend '''

class Client:
	def __init__(self):
		client = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", port=54321))
		# result = client.call('conc', 'aa', 'bb')  # = > 3
		print(result)

	def send_paths(*pathlist):
		print(pathlist)