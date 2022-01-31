

CHUNK_SIZE = 2**14
RECV_PORT = 9990
RECV_IP = '0.0.0.0'

def get_server(ip,port):
	import socket

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((RECV_IP, RECV_PORT))
	sock.listen(5)
	print('Serving  on port %s.' % (sock.getsockname()[1],))

	return sock

def get_filename(name):
	# content = [i for i in f.read().split('\'') if i!=''and i!=' ']
	return name.split('/')[-1]


def recieve(_sock):
	saperator = b'<SAPERATOR>'
	print('Recieving File')
	# outputf = open(i,'wb')
	outputf = ''

	while True:
		chunk = _sock.recv(CHUNK_SIZE)
		if not chunk:
			outputf.close()
			break
		if saperator in chunk:
			filename,chunk = chunk.split(saperator)

			outputf = open(get_filename(filename.decode()),'wb')
			print(f'Recieving {get_filename(filename.decode())}')
		outputf.write(chunk)

		# if data==b'next':
		# outputf.close()


	_sock.close()

def recieveFile(Connection):
	while True:
		_sock, addr = Connection.accept()
		print("Incoming Data from : ", addr)


		recieve(_sock)
		_sock.close()


# recieveFile(sock)