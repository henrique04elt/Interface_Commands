import socket

def start_server():
    TCP_IP = '0.0.0.0'
    TCP_PORT = 55502
    BUFFER_SIZE = 5048

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((TCP_IP, TCP_PORT))
    server_socket.listen(1)
    print("Servidor aguardando conexões...")

    conn, addr = server_socket.accept()
    print('Conexão estabelecida com:', addr)

    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            print("Dados recebidos:", data.hex())
            response = bytes.fromhex('')  # Resposta de exemplo
            conn.send(response)
            print("Resposta enviada:", response.hex())
    except Exception as e:
        print("Erro:", e)
    finally:
        conn.close()
        server_socket.close()
        print("Conexão fechada.")

if __name__ == "__main__":
    start_server()
