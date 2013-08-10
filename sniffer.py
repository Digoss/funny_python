from scapy.all import *

def PacketHandler(pkt) :
 
  if pkt.haslayer(Dot11) :
		if pkt.type == 0 and pkt.subtype == 8 and pkt.info == 'PORTAL' :
			print "AP MAC: %s with SSID: %s " % (pkt.addr2, pkt.info)
 
 
sniff(iface="mon0", prn = PacketHandler)