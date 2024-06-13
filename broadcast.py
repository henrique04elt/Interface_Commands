import socket
from time import sleep
import sys
def broad():
    interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
    allips = [ip[-1][0] for ip in interfaces]
    msg1 = b'RMC'
    msg2 = b'AD'

    #msg = str.encode(sys.argv[1])
    while True:
        for ip in allips:
            print(f'sending {msg1} on {ip}')
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind((ip,0))
            sock.sendto(msg1, ("255.255.255.255", 44404))
            sock.close()
        sleep(25)
        for ip in allips:
            print(f'sending {msg2} on {ip}')
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind((ip,0))
            sock.sendto(msg2, ("255.255.255.255", 44404))
            sock.close()
        sleep(25)
broad()