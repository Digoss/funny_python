#Socket server

import socket
import sys
import argparse
from thread import *

def init_server(host, port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		print "Failed to create socket. Error code: "+str(msg[0])+" , Error message: "+str(msg[1])
		sys.exit()

	try:
		s.bind((host, port))
	except socket.error, msg:
		print "Bind failed. Error code: "+str(msg[0])+" Message"+msg[1]
		sys.exit()

	print "Socket bind complete"

	s.listen(10)
	print "Socket now listening"

	while True:
		try:
			(conn, addr) = s.accept()
			print "Connected with "+addr[0]+":"+str(addr[1])
			start_new_thread(clienthandler, (conn,))
		except KeyboardInterrupt:
			s.close()
			sys.exit()
	s.close()

def clienthandler(conn):
	conn.send("Welcome to the server. Type something and hit enter\n")
	while True:
		data = conn.recv(1024)
		reply = "OK..."+data
		if not data:
			break
		conn.sendall(reply)
	conn.close()

def argparsefunction():
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--port", help="specify the port to connect", type=int, required=True)
	parser.add_argument("-H", "--host", help="specify the host to connect", default="")

def main():

	
	args = argparsefunction()

	init_server(args.host, args.port)

if __name__ == "__main__":
	main()