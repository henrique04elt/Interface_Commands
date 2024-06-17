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

def send_tcp_schedule(num):
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

            if num == 0:
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
            elif num == 1:
                conn.sendall(bytes.fromhex(send_data_value))
                print(f"Comando enviado: {send_data_value}")


            data=conn.recv(2048)
            print(f"Resposta recebida: {data.hex()}")
    except ValueError as e:
        print(f"Erro de conversão do comando: {e}")
    except socket.error as e:
        print(f"Erro de socket: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def criar_comando_schedule():
    global campo_comando

    programacao = obter_valores_inseridos()

    if programacao is not None:
        config.comando = "ff 55 10 23"  ## Valor não muda

        for horario, percentagem in programacao:
            config.comando += f" {obter_valor_hex(horario.hour)} {obter_valor_hex(horario.minute)} {obter_valor_hex(percentagem)}"

        checksum = obter_checksum(config.comando)
        config.comando += f" {checksum}"

        send_tcp_schedule(0)

        campo_comando.config(state=tk.NORMAL)
        campo_comando.delete(1.0, tk.END)
        campo_comando.insert(tk.END, config.comando)
        campo_comando.config(state=tk.DISABLED)

def criar_comando_brilho():
    send_tcp_schedule(1)

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
    value = int(float(value))  # Converte o valor do slider para inteiro
    send_data_value = brilho.get(value, {}).get("Send Data", "Valor Desconhecido Send")
    label.config(text=f"Valor do Slider: {value}, Send Data: {send_data_value}")
    #print(send_data_value)

def criar_janela():
    global label
    global horarios_entries
    global percentagens_entries
    global campo_comando

    janela = tk.Tk()
    janela.title("Configuração de Brilho")

    style = ttk.Style()
    style.theme_use("clam")
    style.map("Rounded.TFrame", background=[("active", "#e0e0e0")])

    horarios_entries = []
    percentagens_entries = []

    tk.Label(janela, text="Schedule").grid(row=0, column=0, columnspan=4, pady=(0, 20))
    # schedule_frame = ttk.LabelFrame(janela, text="Schedule", padding=10, style="Rounded.TFrame", height=100)
    # schedule_frame.grid(row=0, column=0, columnspan=5, rowspan=9, padx=0, pady=0, sticky="n")

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

    tk.Label(janela, text="Comando Gerado:").grid(row=7, column=0, padx=5, pady=5)
    campo_comando = tk.Text(janela, height=1, width=80)  # Ajuste a largura conforme necessário
    campo_comando.grid(row=7, column=1, columnspan=3, padx=5, pady=5)
    campo_comando.config(state=tk.DISABLED)

    tk.Label(janela, text="Brilho").grid(row=8, column=0, columnspan=4, pady=(30, 0))

    slider = tk.Scale(janela, from_=10, to=100, orient="horizontal", command=update_label, length=600, tickinterval=10, resolution=10)
    slider.grid(row=9, column=0, columnspan=4, padx=0, pady=10)
    label = tk.Label(janela, text="Valor do Slider: 10, Send Data: ff 55 04 66 01 01 0a ca")
    label.grid(column=0, columnspan=4, padx=20, pady=20)

    janela.mainloop()

if __name__ == "__main__":
    criar_janela()
