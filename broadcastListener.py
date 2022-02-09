import socket
import json

class Listener:
    
    def __init__(self, NAME, BROADCAST_PORT = 9990, BUFFER_SIZE = 2**14):
        self.BROADCAST_PORT = BROADCAST_PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        self.NAME = NAME

    def Connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.BROADCAST_PORT))
        return sock

    def listen(self, conn):
        print("Available Devices")
        profile = None
        address = None
        while True:
            bytesAddressPair = conn.recvfrom(self.BUFFER_SIZE)

            profile = json.loads(bytesAddressPair[0].decode())
            address = bytesAddressPair[1]

            # print(profile,address)
            # if profile["Name"] == self.NAME:
            if profile["Name"] == None:
                continue
            print(profile['Name'])
            break
        return (profile,address)

    def GetPublicDevice(self):
        conn = self.Connection()
        result = self.listen(conn)
        conn.close()

        return result

if __name__ == '__main__':
    l = Listener(NAME="Arc_Nova_13")
    print(l.GetPublicDevice())
