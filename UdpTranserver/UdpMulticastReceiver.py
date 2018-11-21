import socket
import struct

multicast_group = '224.1.1.1'
multicast_port = 5007
all_groups = True

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if all_groups:  # On this port, receives ALL multicast groups
    sock.bind(('', multicast_port))

else:  # on this port, listen ONLY to MCAST_GRP
    sock.bind((multicast_group, multicast_port))

mreq = struct.pack("4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    print sock.recv(10240)