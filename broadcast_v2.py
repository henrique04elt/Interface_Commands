import socket
from time import sleep

def broad():
    interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
    allips = [ip[-1][0] for ip in interfaces]
    msgs = [b'RMC', b'AD', b'MODEM', b'NUC']


    while True:






        
        for msg in msgs:
            for ip in allips:
                print(f'sending {msg} on {ip}')
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.bind((ip, 0))
                sock.sendto(msg, ("255.255.255.255", 44404))
                sock.close()
            sleep(25)

broad()
