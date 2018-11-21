import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
for i in range(10):
    message = MESSAGE + " " + str(i)
    sock.sendto(message, (UDP_IP, UDP_PORT))

print "\nAll messages send!"
