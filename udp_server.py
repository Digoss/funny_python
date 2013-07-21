import socket
import sys
import argparse
from parse_arguments import argParseFunction

def createSocket(host, port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print "Socket created"
	except socket.error, msg:
		print "Failed to create socket. Error code: "+str(msg[0])+". Message "+msg[1]
		sys.exit()

	try:
		s.bind((host, port))
		print "Waiting on port: "+str(port)
	except socket.error, msg:
		print "Failed to bind socket. Error code: "+str(msg[0])+". Message "+msg[1]
		sys.exit()

	print "Socket bind complete"

	while True:
		(data, addr) = s.recvfrom(1024)
		
		if not data:
			break

		reply = "OK..."+data

		s.sendto(reply, addr)
		print "Message["+addr[0]+":"+str(addr[1])+"] - "+data.strip()

	s.close()

def main():

	args = argParseFunction()
	try:
		createSocket(args.host, args.port)
	except KeyboardInterrupt:
		sys.exit()

if __name__ == "__main__":
	main()