#Socket server

import socket
import sys
import argparse
import select

def initServer(host, port):

	CONNECTION_LIST = []

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		print "Failed to create socket. Error code: "+str(msg[0])+" , Error message: "+str(msg[1])
		sys.exit()

	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	try:
		s.bind((host, port))
	except socket.error, msg:
		print "Bind failed. Error code: "+str(msg[0])+" Message"+msg[1]
		sys.exit()

	print "Socket bind complete"

	s.listen(10)
	print "Socket now listening"

	CONNECTION_LIST.append(s)

	while True:

		(readfds, writefds, exceptfds) = select.select(CONNECTION_LIST, [], [])

		for sock in readfds:
			if sock == s:
				(conn, addr) = s.accept()
				CONNECTION_LIST.append(conn)
				print "Connected with client %s:%s" % addr
				conn.send("Welcome to the server. Type something and hit enter\n")
			else:
				try:
					clientHandler(sock)
				except:
					CONNECTION_LIST.remove(sock)
					continue
	s.close()

def clientHandler(conn):
	data = conn.recv(1024)
	reply = "OK..."+data
	if data:
		conn.send(reply)

def argParseFunction():
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--port", help="specify the port to connect", type=int, required=True)
	parser.add_argument("-H", "--host", help="specify the host to connect", default="")
	return parser.parse_args()

def main():

	args = argParseFunction()

	try:
		initServer(args.host, args.port)
	except KeyboardInterrupt:
		sys.exit()

if __name__ == "__main__":
	main()