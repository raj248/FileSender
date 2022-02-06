class Receiver:
	def __init__(self, BUFFER_SIZE = 2**14, RECV_PORT = 9990, RECV_IP = '0.0.0.0', SAPERATOR = b'<SAPERATOR>'):
		self.BUFFER_SIZE = BUFFER_SIZE
		self.RECV_PORT = RECV_PORT
		self.RECV_IP = RECV_IP
		self.SAPERATOR = SAPERATOR      


	def Connection(self):
		import socket

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind((self.RECV_IP, self.RECV_PORT))
		sock.listen(5)
		print('Serving  on port %s.' % (sock.getsockname()[1],))

		return sock

	def get_filename(self, name):
		# content = [i for i in f.read().split('\'') if i!=''and i!=' ']
		return name.split('/')[-1]


	def Receive(self, _sock):
		SAPERATOR = b'<SAPERATOR>'
		print('Recieving File')
		# outputf = open(i,'wb')
		outputf = ''

		while True:
			chunk = _sock.recv(self.BUFFER_SIZE)
			if not chunk:
				outputf.close()
				break
			if SAPERATOR in chunk:
				filename,chunk = chunk.split(SAPERATOR)

				outputf = open(self.get_filename(filename.decode()),'wb')
				print(f'Recieving {self.get_filename(filename.decode())}')
			outputf.write(chunk)

			# if data==b'next':
			# outputf.close()


		_sock.close()

	def ReceiveFile(self):
		conn = self.Connection()
		while True:
			_sock, addr = conn.accept()
			print("Incoming Data from : ", addr)


			self.Receive(_sock)
			_sock.close()


if __name__ == '__main__':
	recv = Receiver()
	recv.ReceiveFile()
