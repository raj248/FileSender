import socket
import os

class Sender:
    def __init__(self, BUFFER_SIZE = 2**14, SAPERATOR = b'<SAPERATOR>'):
        self.BUFFER_SIZE = BUFFER_SIZE
        self.SAPERATOR = SAPERATOR      

    def connect(self,address):
        """Connect to the given server and return a non-blocking socket."""

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        # sock.setblocking(0)
        return sock

    def GetFiles(self,filename):
        if not os.path.isdir(filename):
            with open(filename,'r') as f:
                content = [i for i in f.read().split('\'') if i!=''and i!=' ']
                return content
        else:
            return [filename + i for i in os.listdir(filename)]


    def EmptyContent(self, filename):
        with open(filename,'w'):
            pass

    def Sendfile(self, addressPostPair):
        content = self.GetFiles('content.txt')
        if not content:
            content = self.GetFiles('../Send/')
        # print(content)
        if not content:
            return
        for i in content:

            s = self.connect(addressPostPair)
            print('Sending ',i.split('/')[-1])
            inputf = open(i,'rb')
            s.send(bytes(i.encode())+self.SAPERATOR)
            while True:
                chunk = inputf.read(self.BUFFER_SIZE)
                if not chunk:
                    print({i.split('/')[-1]}, 'SENT')
                    s.send(b'<END>')
                    s.close()
                    inputf.close()
                    break


                try:
                    # s.send(chunk) 
                    s.sendall(chunk) 
                except socket.error:
                    s.close()
                    return
        self.EmptyContent('content.txt')


if __name__ == '__main__':
    send = Sender()
    send.Sendfile(('192.168.0.109', 9990))

