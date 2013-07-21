import sys
import socket
import argparse
from parse_arguments import argParseFunction

def createSocket(host, port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print "Socket created"
	except socket.error, msg:
		print "Failed to create socket. Error code: "+str(msg[0])+". Message "+msg[1]
		sys.exit()

	while True:
		msg = raw_input("Enter your message: ")
		try:
			s.sendto(msg, (host,port))
			(data, addr) = s.recvfrom(1024)
			print "Server reply: "+data
		except socket.error, msg:
			print "Error code: "+str(msg[0])+". Message "+msg[1]
			sys.exit()

def main():

	args = argParseFunction()
	try:
		createSocket(args.host, args.port)
	except KeyboardInterrupt:
		sys.exit()

if __name__ == "__main__":
	main()