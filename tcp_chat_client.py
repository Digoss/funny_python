import sys
import socket
import select
from parse_arguments import *

def sheelUsage():
	sys.stdout.write("Me: ")
	sys.stdout.flush()

def initChat(host, port):
	try:
		cliendfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		print "Failed to create socket. Error code: "+str(msg[0])+" , Error message: "+str(msg[1])
		sys.exit()
	cliendfd.settimeout(1)

	try:
		cliendfd.connect((host, port))
	except:
		print "Unable to connect"
		sys.exit()

	while True:
		fd_list = [sys.stdin, cliendfd]
		(readfd, writefd, errorfd) = select.select(fd_list, [], [])

		for fd in readfd:
			if fd == cliendfd:
				data = fd.recv(2048)
				if not data:
					print "Disconnected"
					sys.exit()
				else:
					sys.stdout.write(data)
					sheelUsage()
			else:
				data = sys.stdin.readline()
				cliendfd.send(data)
				sheelUsage()

def main():
	args = argParseFunction()
	initChat(args.host, args.port)

if __name__ == "__main__":
	main()