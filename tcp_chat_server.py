from simple_reply_server import *

def broadcast_message(sock, message):
	for socke in CONNECTION_LIST:
		if socke != getServerSocket() and socke != sock:
			try:
				socke.send(message)
			except:
				CONNECTION_LIST.remove(socke)
				socke.close()
				continue


def main():

	args = argParseFunction()

	try:
		initServer(args.host, args.port, callback=broadcast_message)
	except KeyboardInterrupt:
		print "Ctrl+C pressed!!!"
		sys.exit()

if __name__ == "__main__":
	main()