import socket
import sys
from struct import *
from in_cksum import *

#from parse_arguments import *

def createIPHeader(s_address, d_address):
	source_ip = s_address
	dest_ip = d_address
	ip_ihl = 5
	ip_ver = 4
	ip_tos = 0
	ip_tot_len = 0
	ip_id = 54321
	ip_frag_off = 0
	ip_ttl = 255
	ip_proto = socket.IPPROTO_TCP
	ip_check = 0
	ip_saddr = socket.inet_aton(source_ip)
	ip_daddr = socket.inet_aton(dest_ip)
	ip_ihl_ver = (ip_ver << 4) + ip_ihl

	ip_header = pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)
	return ip_header

def createTCPHeader(s_port, d_port, ck_sum_header, tcp_urg_ptr):
	tcp_source = s_port
	tcp_dest = d_port
	tcp_seq = 454
	tcp_ack_seq = 0
	tcp_doff = 4
	tcp_fin = 0
	tcp_syn = 1
	tcp_rst = 0
	tcp_psh = 0
	tcp_ack = 0
	tcp_urg = 0
	tcp_window = socket.htons(5840)
	tcp_offset_res = (tcp_doff << 4) + 0
	tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)
	tcp_header = pack('!HHLLBBH' ,tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window) + pack("H", ck_sum_header) + pack("!H", tcp_urg_ptr)
	return tcp_header


def createCKSumTCPHeader(s_port, d_port):
	tcp_source = s_port
	tcp_dest = d_port
	tcp_seq = 454
	tcp_ack_seq = 0
	tcp_doff = 4
	tcp_fin = 0
	tcp_syn = 1
	tcp_rst = 0
	tcp_psh = 0
	tcp_ack = 0
	tcp_urg = 0
	tcp_window = socket.htons(5840)
	tcp_check = 0
	tcp_urg_ptr = 0
	tcp_offset_res = (tcp_doff << 4) + 0
	tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)
	tcp_header = pack('!HHLLBBHHH' ,tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window, tcp_check, tcp_urg_ptr)
	return tcp_header

def pseudoHeader(s_address, d_address, tcp_header, data):
	source_address = socket.inet_aton(s_address)
	destination_address = socket.inet_aton(d_address)
	placeholder = 0
	protocol = socket.IPPROTO_TCP
	tcp_length = len(tcp_header) + len(data)
	psh = pack("!4s4sBBH", source_address, destination_address, placeholder, protocol, tcp_length)
	psh = psh + tcp_header + data
	tcp_checksum = checksum(psh)
	return tcp_checksum

def buildPacket(s_address, d_address, s_port, d_port, message):
	ip_header = createIPHeader(s_address, d_address)
	tcp_ck_sum_header = createCKSumTCPHeader(s_port, d_port)
	ck_header = pseudoHeader(s_address, d_address, tcp_ck_sum_header, message)
	tcp_header = createTCPHeader(s_port, d_port, ck_header, 0)
	packet = ip_header + tcp_header + message
	return packet

def sendPacket(fd, packet, dest_ip):
	fd.sendto(packet, (dest_ip, 12345))

def createSocket():
	try:
		sfd = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
	except socket.error, msg:
		print "Socket couldn't be created. Error Code: %s Message: %s" % (str(msg[0]), msg[1])
		sys.exit()

	return sfd

def main():

	#args = argParseFunction()

	fd = createSocket()
	packet = buildPacket("10.1.1.2", "10.1.1.1", 54321, 80, "Hello, how are you")
	for i in range(5):
		sendPacket(fd, packet, "10.1.1.2")


if __name__ == "__main__":
	main()