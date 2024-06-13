import socket

def decode_bytes(data):
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return data.decode('utf-8', 'ignore')

TCP_IP = '10.130.10.10'
TCP_PORT = 55502
BUFFER_SIZE = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print('Waiting for connection...')
conn, addr = s.accept()
print('Connection address:', addr)

while True:
    data = conn.recv(BUFFER_SIZE)
    if not data:
        break
    print("Received data:", data)

    data_str = decode_bytes(data)
    print("Decoded data:", data_str)

    # Identificar os campos x11, x13 e x14
    x11 = data_str[data_str.find('<APP>') : data_str.find('BV') + 2] if '<APP>' in data_str else None
    x13 = data_str[data_str.find('fan_ctrl_vxxx') : data_str.find('fan_ctrl_vxxx') + 12] if 'fan_ctrl_vxxx' in data_str else None
    x14_values = [x.strip() for x in data_str.split(',') if x.startswith('V')]
    x14 = ','.join(x14_values) if x14_values else None

    print("x11:", x11)
    print("x13:", x13)
    print("x14:", x14)

conn.close()
