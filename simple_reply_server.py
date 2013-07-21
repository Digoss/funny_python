#Socket server

import socket
import sys
import select
from parse_arguments import argParseFunction

CONNECTION_LIST = []
serverSocket = None

def initSocket(host, port):
	global serverSocket
	global CONNECTION_LIST
	try:
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		print "Failed to create socket. Error code: "+str(msg[0])+" , Error message: "+str(msg[1])
		sys.exit()

	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	try:
		serverSocket.bind((host, port))
	except socket.error, msg:
		print "Bind failed. Error code: "+str(msg[0])+" Message"+msg[1]
		sys.exit()

	print "Socket bind complete"

	serverSocket.listen(10)
	print "Socket now listening"

	CONNECTION_LIST.append(serverSocket)


def initServer(host, port, callback):

	initSocket(host, port)

	while True:
		(readfds, writefds, exceptfds) = select.select(CONNECTION_LIST, [], [])
		for sock in readfds:
			if sock == serverSocket:
				(conn, addr) = serverSocket.accept()
				CONNECTION_LIST.append(conn)
				print "Connected with client %s:%s" % addr
				conn.send("Welcome to the server. Type something and hit enter\n")
				if callable(callback):
					callback(conn, "Client %s:%s entered room\n" % addr)
			else:
				try:
					data = sock.recv(1024)
					if len(data) == 0:
						closeConnection(sock)
						continue
					if callable(callback):
						callback(sock, data)
					else:
						print "callback is not defined"
						print "Simple client handler call will be used"
						clientHandler(sock, data)
				except:
						closeConnection(sock)
						continue

	serverSocket.close()


def clientHandler(conn, message):
	reply = "OK..."+message
	if message:
		conn.send(reply)

def getServerSocket():
	return serverSocket

def closeConnection(socket):
	socket.close()
	CONNECTION_LIST.remove(socket)


def main(callback):

	args = argParseFunction()
	callback(1)

	try:
		initServer(args.host, args.port)
	except KeyboardInterrupt:
		sys.exit()


if __name__ == "__main__":
	main()