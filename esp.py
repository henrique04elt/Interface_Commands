import socket

def find_esp32_ip():
    esp32_ip = None
    target_port = 44406

    # Criar um socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)  # Definir um tempo limite para a resposta

    # Enviar uma mensagem de descoberta para a porta do ESP32
    sock.sendto(b"discover", ("<broadcast>", target_port))

    try:
        # Esperar por uma resposta do ESP32
        data, addr = sock.recvfrom(1024)
        esp32_ip = addr[0]
    except socket.timeout:
        print("Nenhum dispositivo ESP32 encontrado na rede")

    sock.close()
    return esp32_ip

# Encontrar o endereço IP do ESP32
esp32_ip = find_esp32_ip()
if esp32_ip:
    print(f"Endereço IP do ESP32 encontrado: {esp32_ip}")
else:
    print("Não foi possível encontrar o endereço IP do ESP32")
