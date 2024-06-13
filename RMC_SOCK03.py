import socket

def decode_bytes(data):
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return data.decode('utf-8', 'ignore')

def parse_data(data_str):
    x11_start = data_str.find('<APP>')
    x11_end = data_str.find('BV', x11_start)
    x11 = data_str[x11_start + 5 : x11_end].strip() if x11_start != -1 and x11_end != -1 else ""

    x13_start = data_str.find('fan_ctrl_vxxx')
    x13_end = x13_start + 12 if x13_start != -1 else -1
    x13 = data_str[x13_start : x13_end].strip() if x13_start != -1 else ""

    x14_values = [x.strip() for x in data_str.split(',') if x.startswith('V')]
    x14 = ','.join(x14_values) if x14_values else ""
    return x11, x13, x14

def update_html(x11, x13, x14):
    with open("data_display.html", "w", encoding="utf-8") as f:  # Especificando a codificação como UTF-8
        f.write(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dados Recebidos</title>
        </head>
        <body>
            <h1>Dados Recebidos</h1>
            <p>x11: {x11}</p>
            <p>x13: {x13}</p>
            <p>x14: {x14}</p>
        </body>
        </html>
        """)

TCP_IP = '192.168.0.197'
TCP_PORT = 55502
BUFFER_SIZE = 1024
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
    x11, x13, x14 = parse_data(data_str)

    print("x11:", x11)
    print("x13:", x13)
    print("x14:", x14)

    update_html(x11, x13, x14)

conn.close()
