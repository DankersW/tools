import socket
import time

multicast_group = '224.1.1.1'
multicast_port = 5007
content = "Hello from the other side! "
multicast_TTL = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, multicast_TTL)

for i in range(1000):
    # message = content + str(i)
    message = str(i)
    sock.sendto(message, (multicast_group, multicast_port))
    print "Message: " + message
    time.sleep(0.01)