import socket
import time

TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Yo, What Up?".encode()

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((TCP_IP, TCP_PORT))


while 1:
	time.sleep(25)
	soc.send(MESSAGE)
	data = soc.recv(BUFFER_SIZE)
	if(data == "done"):
		soc.close()
	print("Received Data: ", data.decode())