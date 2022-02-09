from broadcast import Broadcast
from broadcastListener import Listener
from Receive import Receiver
from Send import Sender
import multiprocessing
import json

NAME = None
RECV_PORT = None
RECV_IP = None
BROADCAST_PORT = 9990
BUFFER_SIZE = 2**14  # 16384 bytes
SAPERATOR = b'<SAPERATOR>'

def Profile():
	with open('profile.json') as f:
		return json.loads(f.read())

def Initialize():
	global NAME, RECV_PORT ,RECV_IP ,BROADCAST_PORT ,BUFFER_SIZE 
	profile = Profile()
	NAME = profile['Name']
	RECV_PORT = profile['RECV_PORT']
	RECV_IP = profile['RECV_IP']
	BROADCAST_PORT = profile['BROADCAST_PORT']
	BUFFER_SIZE = int(profile['BUFFER_SIZE'])

def StartService():
	Initialize()
	broadcast = Broadcast(BROADCAST_PORT = BROADCAST_PORT)

	receiver = Receiver(BUFFER_SIZE = BUFFER_SIZE, 
						RECV_PORT = RECV_PORT, 
						RECV_IP = RECV_IP
						)
	
	broadcast.Start()
	multiprocessing.Process(target=receiver.ReceiveFile,args=()).start()

def Send():
	Initialize()
	listener = Listener(NAME=NAME)
	device,(ip,_) = listener.GetPublicDevice()
	sender = Sender()
	sender.Sendfile((ip,device["RECV_PORT"]))
	# print(device,ip)


StartService()


