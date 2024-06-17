## Programa para geração de código para Schedule de Brilho         ##
## Henrique Rosa & Henrique Romera                                 ##
## Data : 17/06/2024                                               ##
## Schedule_RMC_V2                                                 ##
## V2.1:                                                             ##
## Função send_tcp_schedule: envia um comando via socket para      ##
## definir um schedule de brilho, desabilitando o backlight        ##
## automático e ativando o schedule                                ##
## Função criar_comando_schedule: chama a função send_tcp_schedule ##
## V2.1:                                                                     ##
## Tradução de itens para PT-BR                                              ##

import tkinter as tk
from datetime import datetime, time
import config
import socket
import time

def obter_valor_hex(valor):
    if isinstance(valor, int):
        return format(valor, '02x')
    elif isinstance(valor, str) and valor.startswith('0x'):
        return valor
    else:
        return format(int(valor), '02x')

def send_tcp_schedule():
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
            data = conn.recv(2048)
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

        send_tcp_schedule()

        campo_comando.config(state=tk.NORMAL)
        campo_comando.delete(1.0, tk.END)
        campo_comando.insert(tk.END, config.comando)
        campo_comando.config(state=tk.DISABLED)



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

def criar_janela():
    global horarios_entries
    global percentagens_entries
    global campo_comando

    janela = tk.Tk()
    janela.title("Configuração da Schedule de Brilho")

    horarios_entries = []
    percentagens_entries = []

    for i in range(5):
        tk.Label(janela, text=f"{i+1}º horário: (hh:mm)").grid(row=i, column=0, padx=5, pady=5)
        horario_entry = tk.Entry(janela)
        horario_entry.grid(row=i, column=1, padx=5, pady=5)
        horarios_entries.append(horario_entry)

        tk.Label(janela, text="Porcentagem:").grid(row=i, column=2, padx=5, pady=5)
        tk.Label(janela, text="%").grid(row=i, column=4, padx=5, pady=5)
        percentagem_entry = tk.Entry(janela)
        percentagem_entry.grid(row=i, column=3, padx=5, pady=5)
        percentagens_entries.append(percentagem_entry)

    botao_criar_comando = tk.Button(janela, text="Enviar Schedule", command=criar_comando_schedule)
    botao_criar_comando.grid(row=5, columnspan=4, pady=10)

    tk.Label(janela, text="Comando Gerado:").grid(row=6, column=0, padx=5, pady=5)
    campo_comando = tk.Text(janela, height=1, width=80)  # Ajuste a largura conforme necessário
    campo_comando.grid(row=6, column=1, columnspan=3, padx=5, pady=5)
    campo_comando.config(state=tk.DISABLED)

    janela.mainloop()

if __name__ == "__main__":
    criar_janela()
