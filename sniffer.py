from scapy.all import *

# def pktPrint(pkt):
# 	if pkt.haslayer(TCP):
# 		print '[+] Detected a TCP Packet'
# 	if pkt.haslayer(Raw):
# 		pass
# 		#payload = pkt.getlayer(Raw).load

# sniff(iface='mon0', prn=pktPrint)

# ap_list = []
 
def PacketHandler(pkt) :
 
  if pkt.haslayer(Dot11) :
		if pkt.type == 0 and pkt.subtype == 8 and pkt.info == 'PORTAL' :
			print "AP MAC: %s with SSID: %s " % (pkt.addr2, pkt.info)
 
 
sniff(iface="mon0", prn = PacketHandler)