import socket

CHUNK_SIZE = 2**14

def connect(address):
    """Connect to the given server and return a non-blocking socket."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    # sock.setblocking(0)
    return sock



def Sendfile(content:[], address):
    saperator = b'<SAPERATOR>'
    for i in content:

        s = connect(address)
        print('Sending ',i)
        inputf = open(i,'rb')
        s.send(bytes(i.encode())+saperator)
        while True:
            chunk = inputf.read(CHUNK_SIZE)
            if not chunk :
                print(f'{i} has been sent')
                # s.close()
                s.send(b'')
                inputf.close()
                break

            # print('Sending %d bytes' % len(chunk))

            try:
                s.sendall(chunk) 
            except socket.error:
                s.close()
                return
        # s.sendall(b'next')

    # s.close()


content = ''
with open('content.txt','r') as f:
    content = [i for i in f.read().split('\'') if i!=''and i!=' ']
Sendfile(content,('192.168.0.100', 9990))