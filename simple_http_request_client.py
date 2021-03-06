#Socket client

import socket
import sys
import argparse
from parse_arguments import argParseFunction

def initClient(host, port):

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		print "Failed to create socket. Error code: "+str(msg[0])+" , Error message: "+str(msg[1])
		sys.exit()

	print "Socket Created"

	try:
		remote_ip = socket.gethostbyname(host)
	except socket.gaierror:
		print "Hostname could not be resolved. Exiting"
		sys.exit()

	print 'Ip address of '+host+' is '+remote_ip

	s.connect((remote_ip,port))

	print "Socket connected to "+host+" on ip "+remote_ip

	message = "GET / HTTP/1.1\r\n\r\n"

	try:
		s.sendall(message)
	except socket.error:
		print "Send Failed"
		sys.exit()
	print "Message send successfully"

	reply = s.recv(4096)
	print reply

	s.close()

	print "Socket closed"

def main():

	args = argParseFunction()

	initClient(args.host, args.port)

if __name__ == "__main__":
	main()