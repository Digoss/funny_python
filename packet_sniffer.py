import socket
import sys
from struct import *

def createSocket():
	try:
		fd = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
	except socket.error, msg:
		print "Socket create. Error: %d, Message %d" % (str(msg[0]), msg[1])
	return fd

def parseIPHeader(pkt):
	ip_packet = unpack("!BBHHHBBH4s4s", pkt)
	version_ihl = ip_packet[0]
	version = (version_ihl >> 4)
	ihl = version_ihl & 0xF
	iph_length = ihl * 4
	ttl = ip_packet[5]
	protocol = ip_packet[6]
	s_addr = socket.inet_ntoa(ip_packet[8])
	d_addr = socket.inet_ntoa(ip_packet[9])
	print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)
	return iph_length

def parseTCPHeader(pkt):
	tcp_packet = unpack("!HHLLBBHHH", pkt)
	s_port = tcp_packet[0]
	d_port = tcp_packet[1]
	seq = tcp_packet[2]
	ack = tcp_packet[3]
	doff_reserved = tcp_packet[4]
	tcp_length = doff_reserved >> 4
	print 'Source Port : ' + str(s_port) + ' Dest Port : ' + str(d_port) + ' Sequence Number : ' + str(seq) + ' Acknowledgement : ' + str(ack) + ' TCP header length : ' + str(tcp_length)
	return tcp_length

def parseData(pkt):
	print "Data: " + pkt


def initSniffer():
	sock = createSocket()
	try:
		while True:
			packet = sock.recvfrom(65565)
			packet = packet[0]
			ip_header = packet[0:20]
			ip_size = parseIPHeader(ip_header)
			tcp_header = packet[ip_size:ip_size+20]
			tcp_size = parseTCPHeader(tcp_header)
			header_size = ip_size + tcp_size * 4
			data_size = len(packet) - header_size
			parseData(packet[data_size:])

	except KeyboardInterrupt:
		print "Closing"
		sock.close()
		sys.exit()

def main():
	initSniffer()

if __name__ == "__main__":
	main()
