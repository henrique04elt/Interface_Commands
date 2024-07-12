## Programa para geração de código para Schedule de Brilho         ##
## Henrique Rosa & Henrique Romera                                 ##
## Data : 17/06/2024                                               ##
## Schedule_RMC_V3                                                 ##
## V3.0:                                                           ##
## Implementação de slider para definir brilho do BOE              ##


import tkinter as tk
from tkinter import ttk
from datetime import datetime, time
import config
import socket
import time
from boe import brilho


def obter_valor_hex(valor):
    if isinstance(valor, int):
        return format(valor, '02x')
    elif isinstance(valor, str) and valor.startswith('0x'):
        return valor
    else:
        return format(int(valor), '02x')

def send_tcp_brilho(num):
    global send_data_value
    ip = config.ip_entry.get()
    port = config.port_entry.get()

    if not ip or not port:
        print("IP ou Porta não fornecido.")
        return
    try:
        port = int(port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ip, port))
            s.listen(1)
            conn, addr = s.accept()
            print('Connection address:', addr)
            # print(f"Conectando a {ip}:{port}")
            # s.connect((ip, port))

            if num == 0: #comandos schedule
                print(config.comando)
                comando_bl = "ff 55 04 21 01 02 00 7c"
                conn.sendall(bytes.fromhex(comando_bl))
                print(f"Comando enviado: {comando_bl}")
                time.sleep(1)
                comando_sche = "ff 55 04 29 01 02 01 85"
                conn.sendall(bytes.fromhex(comando_sche))
                print(f"Comando enviado: {comando_sche}")
                time.sleep(1)
                conn.sendall(bytes.fromhex(config.comando))
                print(f"Comando enviado: {config.comando}")
            elif num == 1: #comandos brilho
                print(send_data_value)
                conn.sendall(bytes.fromhex(send_data_value))
                print(f"Comando enviado: {send_data_value}")
                # altera_texto_brilho(brilho)

            data=conn.recv(2048)
            print(f"Resposta recebida: {data.hex()}")
    except ValueError as e:
        print(f"Erro de conversão do comando: {e}")
    except socket.error as e:
        print(f"Erro de socket: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def process_hex_data(data):
    header = "ff5504560101"
    # header = "ff5507ae"
    header_length = len(header) // 2  # Length of the header in bytes
    bytes_to_capture = 7  # Total bytes to capture including the header

    header_bytes = bytes.fromhex(header)
    result = []

    # Converting hex string to bytes
    data_bytes = bytes.fromhex(data.hex())

    i = 0
    while i < len(data_bytes):
        # Check if the header is found at the current position
        if data_bytes[i:i + header_length] == header_bytes:
            # Ensure there are enough bytes after the header to capture
            if i + bytes_to_capture <= len(data_bytes):
                result.append(data_bytes[i:i + bytes_to_capture])
                i += bytes_to_capture  # Move index past the 64 bytes
            else:
                break
        else:
            i += 1  # Move to the next byte if header not found

    return result
def get_brilho():
    ip = config.ip_entry.get()
    port = config.port_entry.get()
    if not ip or not port:
        print("IP ou Porta não fornecido.")
        return
    try:
        port = int(port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ip, port))
            s.listen(1)
            conn, addr = s.accept()
            print('Connection address:', addr)
            print(f"Enviando comando: FF 55 04 56 01 01 00 b0")
            conn.sendall(bytes.fromhex("FF 55 04 56 01 01 00 b0"))
            timeout = 5  # Timeout em segundos
            start_time = time.time()
            attempt = 0
            time.sleep(0.1)
            brilho = None
            while 1:
                data = conn.recv(2048)
                print(f"Resposta recebida: {data.hex()}")
                result = process_hex_data(data)
                for packet in result:
                    brilho = str(packet[6])
                    print(brilho)
                    altera_texto_brilho(brilho)

                if time.time() - start_time > timeout:
                    print("Timeout atingido.")
                    attempt += 1
                    if attempt == 5:
                        break
                    print(f"Enviando comando: FF 55 04 56 01 01 00 b0")
                    conn.sendall(bytes.fromhex("FF 55 04 56 01 01 00 b0"))
                    start_time = time.time()
                if brilho is not None:
                    break

    except ValueError as e:
        print(f"Erro de conversão do comando: {e}")
    except socket.error as e:
        print(f"Erro de socket: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def altera_texto_brilho(brilho):
    label_brilho.config(text=f"Brilho = {brilho}")

def criar_comando_schedule():
    global campo_comando

    programacao = obter_valores_inseridos()

    if programacao is not None:
        config.comando = "ff 55 10 23"  ## Valor não muda

        for horario, percentagem in programacao:
            config.comando += f" {obter_valor_hex(horario.hour)} {obter_valor_hex(horario.minute)} {obter_valor_hex(percentagem)}"

        checksum = obter_checksum(config.comando)
        config.comando += f" {checksum}"

        send_tcp_brilho(0)

        campo_comando.config(state=tk.NORMAL)
        campo_comando.delete(1.0, tk.END)
        campo_comando.insert(tk.END, config.comando)
        campo_comando.config(state=tk.DISABLED)

def criar_comando_brilho():
    send_tcp_brilho(1)

def obter_checksum(comando):
    valores = [int(valor, 16) for valor in comando.split()]
    soma = sum(valores) & 0xFF
    checksum = format(soma, '02x')  # Correção no cálculo do checksum Base 8
    return checksum

def obter_valores_inseridos():
    programacao = []

    for i in range(5):
        horario_str = horarios_entries[i].get()
        percentagem_str = percentagens_entries[i].get()

        try:
            horario = datetime.strptime(horario_str, "%H:%M").time()
            percentagem = int(percentagem_str)
        except ValueError:
            tk.messagebox.showerror("Erro", "Certifique-se de inserir valores válidos.")
            return None

        programacao.append((horario, percentagem))

    return programacao

def update_label(value):
    global send_data_value
    """Função para atualizar o texto do label com o valor do slider e 'Send Data' do dicionário baseado no slider."""
    value = int(float(value))  # Converte o valor do slider para inteiro
    tela = selected_tela.get()  # Obtém a tela selecionada no OptionMenu
    send_data_value = brilho.get(tela, {}).get(value, {}).get("Send Data", "Valor Desconhecido")
    # label.config(text=f"Tela: {tela}, Valor do Slider: {value}, Send Data: {send_data_value}")
    # altera_texto_brilho(value)
    # print(tela)
    # print(send_data_value)

def criar_janela():
    global label, selected_tela, label_brilho, horarios_entries, percentagens_entries, campo_comando, send_data_value

    send_data_value = "ff 55 04 66 01 01 0a ca"
    janela = tk.Tk()
    janela.title("Configuração de Brilho")

    style = ttk.Style()
    style.theme_use("clam")
    style.map("Rounded.TFrame", background=[("active", "#e0e0e0")])

    horarios_entries = []
    percentagens_entries = []

    tk.Label(janela, text="Schedule").grid(row=0, column=0, columnspan=4, pady=(0, 20))

    for i in range(5):
        tk.Label(janela, text=f"{i+1}º horário: (hh:mm)").grid(row=i+1, column=0, padx=0, pady=5)
        horario_entry = tk.Entry(janela)
        horario_entry.grid(row=i+1, column=1, padx=0, pady=5)
        horarios_entries.append(horario_entry)

        tk.Label(janela, text="Porcentagem:").grid(row=i+1, column=2, padx=5, pady=5)
        tk.Label(janela, text="%").grid(row=i+1, column=4, padx=5, pady=5)
        percentagem_entry = tk.Entry(janela)
        percentagem_entry.grid(row=i+1, column=3, padx=5, pady=5)
        percentagens_entries.append(percentagem_entry)

    botao_criar_comando = tk.Button(janela, text="Enviar Schedule", command=criar_comando_schedule)
    botao_criar_comando.grid(row=6, columnspan=4, pady=10)

    botao_criar_comando = tk.Button(janela, text="Enviar Brilho", command=criar_comando_brilho)
    botao_criar_comando.grid(row=10, columnspan=4, pady=10)

    botao_get_brilho = tk.Button(janela, text="Get Brilho", command=get_brilho)
    botao_get_brilho.grid(row=10,column = 2, columnspan=4, pady=10)

    tk.Label(janela, text="Comando Gerado:").grid(row=7, column=0, padx=5, pady=5)
    campo_comando = tk.Text(janela, height=1, width=80)  # Ajuste a largura conforme necessário
    campo_comando.grid(row=7, column=1, columnspan=3, padx=5, pady=5)
    campo_comando.config(state=tk.DISABLED)

    tk.Label(janela, text="Brilho").grid(row=8, column=0, columnspan=4, pady=(30, 0))

    frame = tk.Frame(janela)
    frame.grid(row=10, column=1, padx=20, pady=20)

    selected_tela = tk.StringVar(janela, value="Tela 1")
    option_menu = ttk.OptionMenu(
         frame,
         selected_tela,
         "Tela 1",
         *brilho.keys(),
         command=lambda _: update_label(slider.get())
         )
    option_menu.grid(row=10, column=1, pady=20)
    tk.Label(janela, text="Tela:").grid(row=10, column=0, columnspan=2, padx=(0, 30))
    # print(*brilho.keys())

    slider = tk.Scale(janela, from_=10, to=100, orient="horizontal", command=update_label, length=600, tickinterval=10, resolution=10)
    slider.grid(row=9, column=0, columnspan=4, padx=0, pady=10)
    # label = tk.Label(janela, text="Tela: Tela 1, Valor do Slider: 10, Send Data: ff 55 04 66 01 01 0a ca")
    # label.grid(column=0, columnspan=4, padx=20, pady=20)

    label_brilho = tk.Label(janela, text="Brilho = ??")
    label_brilho.grid(row=10, column=3, columnspan=4, padx=20, pady=20)

    # get_brilho()

    janela.mainloop()

if __name__ == "__main__":
    criar_janela()
