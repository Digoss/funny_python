import socket
import sys
from parse_arguments import *
from struct import *

def createIPHeader():
	source_ip = '10.1.1.2'
	dest_ip = '10.1.1.1'
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


def createTCPHeader():
	tcp_source = 1234
	tcp_dest = 80
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



def createSocket():
	try:
		sfd = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
	except socket.error, msg:
		print "Socket couldn't be created. Error Code: %s Message: %s" % str(msg[0]), msg[1]
		sys.exit()

def main():

	args = argParseFunction()

if __name__ == "__main__":
	main()