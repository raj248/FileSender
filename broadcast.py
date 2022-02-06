import socket, time
import json
import threading

class broadcast:
    def __init__(self):
        self.BROADCAST_PORT = 9990
        self.BROADCAST_IP = '255.255.255.255'
        self.SERVER_ADDRESS_PORT = (self.BROADCAST_IP, self.BROADCAST_PORT)
        self.SERVER = True

    def Connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        return sock


    def Profile(self):
        with open('profile.json','r') as f:
            return f.read()


    def Server(self, server, dataToSend):
        while(self.SERVER):
            server.sendto(dataToSend, self.SERVER_ADDRESS_PORT)
            time.sleep(3)
        server.close()

    

    def Start(self):
        server = self.Connection()
        profile = self.Profile()
        dataToSend = profile.encode()
        self.SERVER = True
        threading.Thread(target=self.Server,args=(server, dataToSend)).start()

    def Stop(self):
        self.SERVER = False


b = broadcast()
b.Start()
