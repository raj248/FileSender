class Receiver:
	def __init__(self, BUFFER_SIZE = 2**14, RECV_PORT = 9990, RECV_IP = '0.0.0.0', SAPERATOR = b'<SAPERATOR>'):
		self.BUFFER_SIZE = BUFFER_SIZE
		self.RECV_PORT = RECV_PORT
		self.RECV_IP = RECV_IP
		self.SAPERATOR = SAPERATOR  
		self.RECV_DEST = '/home/bell/Desktop/RECV/'



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

	def fix_ownership(self, path):
		"""Change the owner of the file to SUDO_UID"""
		import os

		uid = os.environ.get('SUDO_UID')
		gid = os.environ.get('SUDO_GID')

		uid = '1000' if not uid else uid
		gid = '1000' if not gid else gid
		if uid is not None:
			os.chown(path, int(uid), int(gid))

	def Receive(self, _sock):
		import time
		print('Recieving File')
		# outputf = open(i,'wb')
		outputf = ''
		buffer = []

		while True:
			chunk = _sock.recv(self.BUFFER_SIZE)
			buffer += chunk.split(b'<END>') if chunk else []
			chunk = buffer.pop(0) if buffer else chunk

			if not chunk and not buffer:

				outputf.close()
				break
			if self.SAPERATOR in chunk:
				filename,chunk = chunk.split(self.SAPERATOR)
				filename = self.RECV_DEST + self.get_filename(filename.decode())
				outputf = open(filename,'wb')

				self.fix_ownership(filename)
				
				print(f'Recieving {filename}')
			outputf.write(chunk)

			# if data==b'next':
			# outputf.close()


		# _sock.close()

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
