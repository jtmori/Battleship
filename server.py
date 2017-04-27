import socket
import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print(self.client_address[0]," wrote:")
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

def GameServerThread():
	TCP_IP = 'localhost'
	TCP_PORT = 5005
	BUFFER_SIZE = 20

	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.bind((TCP_IP, TCP_PORT))
	soc.listen(2) # waits for 2 to join

	conn, addr = soc.accept()
	print("Connection Address: ", addr)

	while 1:
		data = conn.recv(BUFFER_SIZE)
		if(data): 
			print("received data: ", data.decode())
			conn.send(data) #echo
	conn.close()


#GameServerThread()