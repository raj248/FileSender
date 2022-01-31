import socket

bufferSize = 2**14


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 9990))

print("UDP server up and listening")

while(True):

    bytesAddressPair = sock.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    print(f"Hello {address}")
    
    # print(clientMsg)
    # print(clientIP)

print(sock)
sock.close()