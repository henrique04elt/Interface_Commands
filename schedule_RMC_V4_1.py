## Programa para geração de código para Schedule de Brilho         ##
## Henrique Rosa & Henrique Romera                                 ##
## Data : 17/06/2024                                               ##
## Schedule_RMC_V3                                                 ##
## V4.0:                                                           ##
## Implementação de slider para definir brilho do BOE              ##


import tkinter as tk
from tkinter import ttk
from datetime import datetime, time
import config
import socket
import time
import boe


def obter_valor_hex(valor):
    if isinstance(valor, int):
        return format(valor, '02x')
    elif isinstance(valor, str) and valor.startswith('0x'):
        return valor
    else:
        return format(int(valor), '02x')

def send_tcp_brilho(num):
    global send_data_value, selected_tela
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

            if num == 0: #comandos schedule
                comando_bl = "ff 55 04 21 01 02 00 7c"
                conn.sendall(bytes.fromhex(comando_bl))
                print(f"Comando enviado: {comando_bl}")
                time.sleep(1)
                comando_schedule = "ff 55 04 29 01 02 01 85"
                conn.sendall(bytes.fromhex(comando_schedule))
                print(f"Comando enviado: {comando_schedule}")
                time.sleep(1)
                conn.sendall(bytes.fromhex(config.comando))
                print(f"Comando enviado: {config.comando}")
            elif num == 1: #comandos brilho
                conn.sendall(bytes.fromhex(send_data_value))
                print(f"Comando enviado: {send_data_value}")

            elif num == 2:  # comando liga tela
                if selected_tela.get() == "Tela 1":
                    conn.sendall(bytes.fromhex(boe.comandos["Estado da Tela"]["Setting"]["Ligar a Tela 1"]["Send Data"]))
                    print(f"Comando enviado: {boe.comandos["Estado da Tela"]["Setting"]["Ligar a Tela 1"]["Send Data"]}") #ligar tela 1
                elif selected_tela.get() == "Tela 2":
                    conn.sendall(bytes.fromhex(boe.comandos["Estado da Tela"]["Setting"]["Ligar a Tela 2"]["Send Data"]))
                    print(f"Comando enviado: {boe.comandos["Estado da Tela"]["Setting"]["Ligar a Tela 2"]["Send Data"]}") #ligar tela 2
                elif selected_tela.get() == "Telas 1 e 2":
                    conn.sendall(bytes.fromhex(boe.comandos["Estado da Tela"]["Setting"]["Ligar a Tela 1 e 2"]["Send Data"]))
                    print(f"Comando enviado: {boe.comandos["Estado da Tela"]["Setting"]["Ligar a Tela 1 e 2"]["Send Data"]}") #ligar tela 1 e 2
            elif num == 3:  # comandos desliga tela
                if selected_tela.get() == "Tela 1":
                    conn.sendall(bytes.fromhex(boe.comandos["Estado da Tela"]["Setting"]["Desligar a Tela 1"]["Send Data"]))
                    print(f"Comando enviado: {boe.comandos["Estado da Tela"]["Setting"]["Desligar a Tela 1"]["Send Data"]}") #ligar tela 1
                elif selected_tela.get() == "Tela 2":
                    conn.sendall(bytes.fromhex(boe.comandos["Estado da Tela"]["Setting"]["Desligar a Tela 2"]["Send Data"]))
                    print(f"Comando enviado: {boe.comandos["Estado da Tela"]["Setting"]["Desligar a Tela 2"]["Send Data"]}") #ligar tela 2
                elif selected_tela.get() == "Telas 1 e 2":
                    conn.sendall(bytes.fromhex(boe.comandos["Estado da Tela"]["Setting"]["Desligar a Tela 1 e 2"]["Send Data"]))
                    print(f"Comando enviado: {boe.comandos["Estado da Tela"]["Setting"]["Desligar a Tela 1 e 2"]["Send Data"]}") #ligar tela 1 e 2

            data = conn.recv(2048)
            print(f"Resposta recebida: {data.hex()}")
    except ValueError as e:
        print(f"Erro de conversão do comando: {e}")
    except socket.error as e:
        print(f"Erro de socket: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def process_hex_data(data, num):
    if num == 1:
        header = "ff5504560101"
    elif num == 2:
        header = "ff5504560202"
    elif num == 3:
        header = "ff5504570101"
    elif num == 4:
        header = "ff5504570202"
    elif num == 5:
        header = "ff5504420101"
    elif num == 6:
        header = "ff5504420202"

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

def get_brilho(num):
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
            if num == 1:
                print(f"Enviando comando: FF 55 04 56 01 01 00 b0")
                conn.sendall(bytes.fromhex("FF 55 04 56 01 01 00 b0"))
            elif num == 2:
                print(f"Enviando comando: FF 55 04 56 02 02 00 b2")
                conn.sendall(bytes.fromhex("FF 55 04 56 02 02 00 b0"))
            elif num == 3:
                print(f"Enviando comando: {bytes.fromhex(boe.comandos["Input Signal Status"]["Reading"]["Tela 1 on"]["Send Data"])}")
                conn.sendall(bytes.fromhex(boe.comandos["Input Signal Status"]["Reading"]["Tela 1 on"]["Send Data"]))
            elif num == 4:
                print(f"Enviando comando: {bytes.fromhex(boe.comandos["Input Signal Status"]["Reading"]["Tela 2 on"]["Send Data"])}")
                conn.sendall(bytes.fromhex(boe.comandos["Input Signal Status"]["Reading"]["Tela 2 on"]["Send Data"]))
            timeout = 5  # Timeout em segundos
            start_time = time.time()
            attempt = 0
            time.sleep(0.1)
            info = None
            input = None
            i=None
            info_str = ""
            input_str = ""
            while 1:
                data = conn.recv(2048)
                print(f"Resposta recebida: {data.hex()}")
                result = process_hex_data(data, num)
                for packet in result:
                    info = str(packet[6])
                    print(info)
                    if num == 1:
                        label_brilho1.config(text=f"Brilho 1= {info}")
                        i=1
                    elif num == 2:
                        label_brilho2.config(text=f"Brilho 2= {info}")
                        i=1
                    elif num == 5:
                        if info == "1":
                            info_str = "DP"
                        if info == "2":
                            info_str = "HDMI1"
                        if info == "3":
                            info_str = "HDMI2"
                        if input == "1":
                            input_str = "Ligado"
                        if input == "0":
                            input_str = "Desligado"
                        label_input1.config(text=f"Tela 1 em " + info_str + "= " + input_str)
                        i=1
                    elif num == 6:
                        if info == "1":
                            info_str = "DP"
                        if info == "2":
                            info_str = "HDMI1"
                        if info == "3":
                            info_str = "HDMI2"
                        if input == "1":
                            input_str = "Ligado"
                        if input == "0":
                            input_str = "Desligado"
                        label_input2.config(text=f"Tela 2 em " + info_str + "= " + input_str)
                        i=1
                    elif num == 3:
                        start_time = time.time()
                        attempt = 0
                        num = 5
                        input = info
                    elif num == 4:
                        start_time = time.time()
                        attempt = 0
                        num = 6
                        input = info
                        # label_input2.config(text=f"Input 2= {info}")
                if time.time() - start_time > timeout:
                    print("Timeout atingido.")
                    attempt += 1
                    if attempt == 5:
                        if num == 1:
                            label_brilho1.config(text=f"Brilho 1= ERRO!")
                        if num == 2:
                            label_brilho2.config(text=f"Brilho 2= ERRO!")
                        if num == 3 or num == 5:
                            label_input1.config(text=f"Tela 1= ERRO!")
                        if num == 4 or num == 6:
                            label_input2.config(text=f"Tela 2= ERRO!")
                        break
                    if num == 1:
                        print(f"Enviando comando: FF 55 04 56 01 01 00 b0")
                        conn.sendall(bytes.fromhex("FF 55 04 56 01 01 00 b0"))
                    elif num == 2:
                        print(f"Enviando comando: FF 55 04 56 02 02 00 b2")
                        conn.sendall(bytes.fromhex("FF 55 04 56 02 02 00 b0"))
                    elif num == 3:
                        print(
                            f"Enviando comando: {bytes.fromhex(boe.comandos["Input Signal Status"]["Reading"]["Tela 1 on"]["Send Data"])}")
                        conn.sendall(
                            bytes.fromhex(boe.comandos["Input Signal Status"]["Reading"]["Tela 1 on"]["Send Data"]))
                    elif num == 4:
                        print(
                            f"Enviando comando: {bytes.fromhex(boe.comandos["Input Signal Status"]["Reading"]["Tela 2 on"]["Send Data"])}")
                        conn.sendall(
                            bytes.fromhex(boe.comandos["Input Signal Status"]["Reading"]["Tela 2 on"]["Send Data"]))
                    elif num == 5:
                        print(
                            f"Enviando comando: {bytes.fromhex(boe.comandos["Input Source"]["Reading"]["Tela 1"]["Send Data"])}")
                        conn.sendall(
                            bytes.fromhex(boe.comandos["Input Source"]["Reading"]["Tela 1"]["Send Data"]))
                    elif num == 6:
                        print(
                            f"Enviando comando: {bytes.fromhex(boe.comandos["Input Source"]["Reading"]["Tela 2"]["Send Data"])}")
                        conn.sendall(
                            bytes.fromhex(boe.comandos["Input Source"]["Reading"]["Tela 2"]["Send Data"]))
                    start_time = time.time()
                if info is not None and i is not None:
                    break

    except ValueError as e:
        print(f"Erro de conversão do comando: {e}")
    except socket.error as e:
        print(f"Erro de socket: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def liga_tela():
    send_tcp_brilho(2)

def desliga_tela():
    send_tcp_brilho(3)

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
    send_data_value = boe.brilho.get(tela, {}).get(value, {}).get("Send Data", "Valor Desconhecido")
    botao_liga_tela.config(text=f"Ligar a(s) {selected_tela.get()}")
    botao_desliga_tela.config(text=f"Desligar a(s) {selected_tela.get()}")
    # label.config(text=f"Tela: {tela}, Valor do Slider: {value}, Send Data: {send_data_value}")

def get_tela1_brilho():
    get_brilho(1)

def get_tela2_brilho():
    get_brilho(2)

def get_tela1_input():
    get_brilho(3)

def get_tela2_input():
    get_brilho(4)

def criar_janela():
    global label, \
        selected_tela, \
        label_brilho1, \
        label_brilho2, \
        label_input1, \
        label_input2, \
        horarios_entries, \
        percentagens_entries, \
        campo_comando, \
        send_data_value, \
        botao_liga_tela,\
        botao_desliga_tela

    send_data_value = "ff 55 04 66 01 01 0a ca"
    janela = tk.Tk()
    janela.title("Configuração de Brilho V4.0")

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
    botao_criar_comando.grid(row=9, columnspan=4, pady=10)

    botao_get_brilho1 = tk.Button(janela, text="Get Brilho Tela 1", command=get_tela1_brilho)
    botao_get_brilho1.grid(row=10, column=0, pady=10, padx=10)

    label_brilho1 = tk.Label(janela, text="Brilho 1 = ??")
    label_brilho1.grid(row=10, column=1, padx=0, pady=0)

    botao_get_brilho2 = tk.Button(janela, text="Get Brilho Tela 2", command=get_tela2_brilho)
    botao_get_brilho2.grid(row=11, column=0, pady=10, padx=10)

    label_brilho2 = tk.Label(janela, text="Brilho 2 = ??")
    label_brilho2.grid(row=11, column=1, padx=0, pady=0)

    botao_get_input1 = tk.Button(janela, text="Get Input Tela 1", command=get_tela1_input)
    botao_get_input1.grid(row=10, column=2, pady=10, padx=10)

    label_input1 = tk.Label(janela, text="Input 1 = ??")
    label_input1.grid(row=10, column=3, padx=0, pady=0)

    botao_get_input2 = tk.Button(janela, text="Get Input Tela 2", command=get_tela2_input)
    botao_get_input2.grid(row=11, column=2, pady=10, padx=10)

    label_input2 = tk.Label(janela, text="Input 2 = ??")
    label_input2.grid(row=11, column=3, padx=0, pady=0)

    # tk.Label(janela, text="Comando Gerado:").grid(row=7, column=0, padx=5, pady=5)
    # campo_comando = tk.Text(janela, height=1, width=80)  # Ajuste a largura conforme necessário
    # campo_comando.grid(row=7, column=1, columnspan=3, padx=5, pady=5)
    # campo_comando.config(state=tk.DISABLED)

    tk.Label(janela, text="Brilho").grid(row=8, column=0, columnspan=4, pady=(30, 0))

    frame = tk.Frame(janela)
    frame.grid(row=9, column=1, padx=20, pady=0)

    selected_tela = tk.StringVar(janela, value="Tela 1")
    option_menu = ttk.OptionMenu(
         frame,
         selected_tela,
         "Tela 1",
         *boe.brilho.keys(),
         command=lambda _: update_label(slider.get())
         )
    option_menu.grid(row=9, column=1, pady=20)
    tk.Label(janela, text="Tela:").grid(row=9, column=0, columnspan=2, padx=(0, 30))

    botao_liga_tela = tk.Button(janela, text=f"Ligar a(s) {selected_tela.get()}", command=liga_tela, width=40)
    botao_liga_tela.grid(row=12, column=0, columnspan=2, pady=10)

    botao_desliga_tela = tk.Button(janela, text=f"Desligar a(s) {selected_tela.get()}", command=desliga_tela, width=40)
    botao_desliga_tela.grid(row=12, column=2, columnspan=2, pady=10)

    slider = tk.Scale(janela,
                      from_=10,
                      to=100,
                      orient="horizontal",
                      command=update_label,
                      length=600,
                      tickinterval=10,
                      resolution=10)
    slider.grid(row=8, column=0, columnspan=4, padx=0, pady=10)

    janela.mainloop()

if __name__ == "__main__":
    criar_janela()
