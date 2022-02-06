import socket
import json

class listener:
    
    def __init__(self):
        self.BROADCAST_PORT = 9990
        self.BUFFER_SIZE = 2**14

    def Connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.BROADCAST_PORT))
        return sock

    def listen(self, conn):

        bytesAddressPair = conn.recvfrom(self.BUFFER_SIZE)

        profile = json.loads(bytesAddressPair[0].decode())
        address = bytesAddressPair[1]

        # print(profile,address)
        return (profile,address)

    def GetPublicDevice(self):
        conn = self.Connection()
        result = self.listen(conn)
        conn.close()

        return result

# l = listener()
# print(l.GetPublicDevice())