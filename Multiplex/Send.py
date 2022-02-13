import socket
import os
import multiprocessing
import time
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print("Finished {} in {} secs".format(repr(func.__name__), round(run_time, 3)))
        return value

    return wrapper

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
    @timer
    def Sendfile(self, addressPortPair, files = None):
        if not files:
            return
        s = self.connect(addressPortPair)



        try:
            while files:
                file = None
                try:
                    file = files.pop(0)
                    print(len(files))
                except:
                    pass
                # s = self.connect(addressPortPair)
                
                print('Sending ',file.split('/')[-1])
                inputf = open(file,'rb')
                s.send(bytes(file.encode())+self.SAPERATOR)
                while True:
                    chunk = inputf.read(self.BUFFER_SIZE)
                    if not chunk:
                        print({file.split('/')[-1]}, 'SENT')
                        s.send(b'<END>')
                        # s.close()
                        inputf.close()
                        break

                    try:
                        # s.send(chunk) 
                        s.sendall(chunk) 
                    except socket.error:
                        s.close()
                        return
        except (BrokenPipeError, IOError) as e:
            print('BrokenPipeError Caught')
            print(e)
            # self.Sendfile(addressPortPair,files)
            pass
        # self.EmptyContent('content.txt')


    def StartMultiplex(self,addressPair,content):
        with multiprocessing.Manager() as manager:
            files = manager.list()
            files+=content
            ports =[addressPair[1]+i for i in range(3)]

            while len(files):

                processes = [multiprocessing.Process(target=self.Sendfile, args = ((addressPair[0],port),files)) for port in ports]

                for process in processes:
                    process.start()
                    time.sleep(1)

    def SendFileMultiplex(self,addressPair):
        content = self.GetFiles('content.txt')
        if not content:
            content = self.GetFiles('../Send/')
        if not content:
            return

        # self.StartMultiplex(addressPair,content)
        with multiprocessing.Manager() as manager:
            files = manager.list()
            files+=content
            ports =[addressPair[1]+i for i in range(3)]

            while len(files):
                processes = [multiprocessing.Process(target=self.Sendfile, args = ((addressPair[0],port),files)) for port in ports]

                for process in processes:
                    process.start()
                    time.sleep(1)



if __name__ == '__main__':
    send = Sender()
    # send.Sendfile(('192.168.0.109', 9990))
    send.SendFileMultiplex(('192.168.0.109', 9990))
    # print(send.GetFiles('content.txt'))

