import socket

TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 20

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((TCP_IP, TCP_PORT))
soc.listen(1)

conn, addr = soc.accept()
print("Connection Address: ", addr)
while 1:
	data = conn.recv(BUFFER_SIZE)
	if not data: break
	print("received data: ", data.decode())
	conn.send(data) #echo
conn.close()