import socket

TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello All!".encode()

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((TCP_IP, TCP_PORT))
soc.send(MESSAGE)

data = soc.recv(BUFFER_SIZE)
soc.close()

print("Received Data: ", data.decode())