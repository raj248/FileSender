import socket, time

bufferSize = 2**14


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print("UDP Sender up and Sending")

bytesToSend = b'Hello'


serverAddressPort = ('255.255.255.255', 9990)
while(True):

    sock.sendto(bytesToSend, serverAddressPort)
    sock.sendto(b'<PING> ', ('255.255.255.255', 9990))

    time.sleep(3)
    

print(sock)
sock.close()