## Programa para controle e testes da RMC com interface gráfica              ##
## Henrique Rosa & Henrique Romera                                           ##
## Data : 17/06/2024                                                         ##
## Interface_RMC_V6.0                                                        ##
## V6.0:                                                                     ##


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import socket
import boe
import threading
import time
from schedule_RMC_V4 import criar_janela
import config
import webbrowser

class CommandInterface:
    def __init__(self, master):
        self.master = master
        master.title("Interface de Comandos BOE V6.1")
        master.geometry("1260x700")

        # Configure estilos e layouts
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configuração do estilo
        self.style.configure("TLabelFrame", background="#f7f7f7", font=("Helvetica", 14), relief="solid", borderwidth=1)
        self.style.configure("TButton", background="#808080", foreground="white", font=("Helvetica", 12), padding=5)
        self.style.configure("TCombobox", font=("Helvetica", 12))
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("TText", font=("Helvetica", 12), wrap="word")
        self.style.configure("Setting.TButton", background="#C0C0C0", foreground="black")
        self.style.configure("Reading.TButton", background="#C0C0C0", foreground="black")
        self.style.configure("Rounded.TFrame", background="#f7f7f7", relief="solid", borderwidth=1)
        self.style.map("Rounded.TFrame", background=[("active", "#e0e0e0")])

        logo_image = Image.open("Eletromidia_logo.png")
        logo_image = logo_image.resize((100, 100))
        self.logo = ImageTk.PhotoImage(logo_image)

        self.logo_label = ttk.Label(master, image=self.logo)
        self.logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.label_frame = ttk.LabelFrame(master, text='Comandos', padding=10, style="Rounded.TFrame")
        self.label_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.command_type_label = ttk.Label(master, text="Tipo de Comando: ", font=("Helvetica", 14))
        self.command_type_label.grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")

        self.show_setting_button = ttk.Button(self.label_frame, text="Comandos de Configuração", style="Setting.TButton", command=self.show_setting_commands)
        self.show_setting_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.show_reading_button = ttk.Button(self.label_frame, text="Comandos de Leitura", style="Reading.TButton", command=self.show_reading_commands)
        self.show_reading_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.command_variable = tk.StringVar(master)
        self.command_variable.set('Selecionar o Comando')

        self.command_menu = ttk.Combobox(self.label_frame, textvariable=self.command_variable, state='readonly', width=40)
        self.command_menu.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky='ew')
        self.command_menu.bind('<<ComboboxSelected>>', self.update_display)

        self.code_frame = ttk.LabelFrame(master, text="Comando", padding=10, style="Rounded.TFrame", height=100)
        self.code_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        self.code_text = tk.Text(self.code_frame, height=3, width=50, font=("Helvetica", 12), bg="#f0f0f0", relief="solid", borderwidth=1)
        self.code_text.pack(fill=tk.BOTH, expand=True)

        self.ack_frame = ttk.LabelFrame(master, text="ACK (Resposta)", padding=10, style="Rounded.TFrame", height=100)
        self.ack_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        self.ack_text = tk.Text(self.ack_frame, height=3, width=50, font=("Helvetica", 12), bg="#f0f0f0", relief="solid", borderwidth=1)
        self.ack_text.pack(fill=tk.BOTH, expand=True)

        self.relay_frame = ttk.LabelFrame(master, text="Controle de Relay", padding=10, style="Rounded.TFrame")
        self.relay_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

        self.schedule_button = ttk.Button(master, text="Configurar Brilho", command=self.abrir_janela_schedule)
        self.schedule_button.grid(row=0, column=0, columnspan=1, pady=10)

        self.web_button = ttk.Button(master, text="Web Browser", command=self.webbrowser)
        self.web_button.grid(row=0, column=1, columnspan=1, pady=140, padx=0)

        self.create_relay_buttons()
        self.relay_status = {i: "OFF" for i in range(6)}

        ip_address = self.get_ip_address()

        self.ip_label = ttk.Label(master, text="IP Address:")
        self.ip_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        config.ip_entry = ttk.Entry(master, width=15)
        config.ip_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        config.ip_entry.insert(0, ip_address)

        self.port_label = ttk.Label(master, text="Port:")
        self.port_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        config.port_entry = ttk.Entry(master, width=15)
        config.port_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        config.port_entry.insert(0, "55502")

        self.send_button = ttk.Button(master, text="Enviar Comando", command=self.send_tcp_command)
        self.send_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10)

        self.get_button = ttk.Button(master, text="Get Data", command=self.get_data)
        self.get_button.grid(row=6, column=1, columnspan=2, pady=10, padx=10)

        version_rmc = bytes.fromhex("20")
        version_fan = bytes.fromhex("20")
        ad_1 = bytes.fromhex("20")
        ad_2 = bytes.fromhex("20")

        self.version_RMC = ttk.Label(master, text="Versão RMC:", width=15)
        self.version_RMC.grid(row=4, column=1, padx=0, pady=5, sticky="e")
        self.version_RMC = ttk.Label(master, text=self.convert_to_ascii(version_rmc), width=15)
        self.version_RMC.grid(row=4, column=2, padx=0, pady=5, sticky="w")

        self.version_FAN = ttk.Label(master, text="Versão FAN:", width=15)
        self.version_FAN.grid(row=5, column=1, padx=0, pady=5, sticky="e")
        self.version_FAN = ttk.Label(master, text=self.convert_to_ascii(version_fan), width=15)
        self.version_FAN.grid(row=5, column=2, padx=0, pady=5, sticky="w")

        self.version_AD1 = ttk.Label(master, text="Versão AD1:", width=15)
        self.version_AD1.grid(row=4, column=2, padx=0, pady=5, sticky="e")
        self.version_AD1 = ttk.Label(master, text=self.convert_to_ascii(ad_1), width=15)
        self.version_AD1.grid(row=4, column=3, padx=0, pady=5, sticky="w")

        self.version_AD2 = ttk.Label(master, text="Versão AD2:", width=15)
        self.version_AD2.grid(row=5, column=2, padx=0, pady=5, sticky="e")
        self.version_AD2 = ttk.Label(master, text=self.convert_to_ascii(ad_2), width=15)
        self.version_AD2.grid(row=5, column=3, padx=0, pady=5, sticky="w")

    def create_relay_buttons(self):
        for i in range(6):
            on_button = ttk.Button(self.relay_frame, text=f"Relay {i} ON", width=15, command=lambda i=i: self.send_relay_command(i, True))
            on_button.grid(row=i, column=0, padx=5, pady=2, sticky="ew")

            off_button = ttk.Button(self.relay_frame, text=f"Relay {i} OFF", width=15, command=lambda i=i: self.send_relay_command(i, False))
            off_button.grid(row=i, column=1, padx=5, pady=2, sticky="ew")

    def send_relay_command(self, relay, turn_on):
        command_type = 'ON' if turn_on else 'OFF'
        command_key = f"Relay - {relay} {command_type}"
        command_data = boe.comandos['Relay']['Setting'].get(command_key, {})

        code = command_data.get('Send Data', 'Code not available')
        ack = command_data.get('ACK', 'ACK not available')

        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, code)

        # self.ack_text.delete("1.0", tk.END)
        # self.ack_text.insert(tk.END, ack)

    def webbrowser(self):
        ip = self.get_ip_address()
        url = 'http://192.168.' + ip[8] + '.237'
        webbrowser.open(url)

    def abrir_janela_schedule(self):
        criar_janela()

    def show_setting_commands(self):
        self.command_type_label.config(text="Tipo de Comando: Configuração")
        self.populate_commands('Setting')

    def show_reading_commands(self):
        self.command_type_label.config(text="Tipo de Comando: Leitura")
        self.populate_commands('Reading')

    def populate_commands(self, command_type):
        self.code_text.delete("1.0", tk.END)
        self.ack_text.delete("1.0", tk.END)

        commands_list = []
        for category, commands in boe.comandos.items():
            if command_type in commands:
                for command in commands[command_type]:
                    commands_list.append(f"{category} - {command}")
        self.command_menu['values'] = commands_list
        if not commands_list:
            self.command_variable.set('No commands found')
        else:
            self.command_variable.set('Selecionar o Comando')

    def update_display(self, event):
        selected_command = self.command_variable.get()
        if ' - ' not in selected_command:
            return

        category, command = selected_command.split(' - ', 1)
        command_data = None

        if category in boe.comandos:
            if 'Setting' in boe.comandos[category] and command in boe.comandos[category]['Setting']:
                command_data = boe.comandos[category]['Setting'][command]
            elif 'Reading' in boe.comandos[category] and command in boe.comandos[category]['Reading']:
                command_data = boe.comandos[category]['Reading'][command]

        if command_data:
            code = command_data.get('Send Data', 'Code not available')
            ack = command_data.get('ACK', 'ACK not available')
        else:
            code = 'Code not available'
            ack = 'ACK not available'

        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, code)

        # self.ack_text.delete("1.0", tk.END)
        # self.ack_text.insert(tk.END, ack)

    def get_ip_address(self):
        hostname = socket.gethostname()
        config.ip_entry = socket.gethostbyname(hostname)
        return config.ip_entry

    def process_ack(self, ack, hex_bytes):
        ack_length = len(ack)
        if ack[:4] == hex_bytes[:4]:
            print(f"ACK {ack.hex()} encontrado no hex fornecido.")
            if len(hex_bytes) >= ack_length:
                following_bytes = hex_bytes[4:ack_length]
                print(f"Próximos {ack_length - 4} bytes após os 4 primeiros bytes: {following_bytes.hex()}")
                self.ack_text.delete("1.0", tk.END)
                self.ack_text.insert(tk.END, ack.hex())
                return 1
            else:
                print("Hex fornecido não possui bytes suficientes após os 4 primeiros bytes do ACK.")
                return 0

    def process_hex_data(self, data):
        headers = [
            ("a1a2a3200011", [6, 5, 5]),  # Header, Lixo, version_rmc
            ("a1a2a3200013", [6, 9, 13]),  # Header, Lixo, version_fan
            ("a1a2a31b0014", [6, 4, 5, 4])  # Header, ad_1, Lixo, ad_2
        ]

        result = []

        # Converting hex string to bytes
        data_bytes = bytes.fromhex(data.hex())

        i = 0
        while i < len(data_bytes):
            matched = False
            for header, sizes in headers:
                header_bytes = bytes.fromhex(header)
                header_length = len(header_bytes)
                if data_bytes[i:i + header_length] == header_bytes:
                    total_length = sum(sizes)
                    if i + total_length <= len(data_bytes):
                        packets = self.divide_into_packets(data_bytes[i:i + total_length], sizes)
                        result.append((header, packets))
                        i += total_length  # Move index past the captured bytes
                    else:
                        i += 1  # Move to the next byte if not enough bytes left
                    matched = True
                    break
            if not matched:
                i += 1  # Move to the next byte if no header matched

        return result

    def divide_into_packets(self, packet, sizes):
        packets = []
        index = 0
        for size in sizes:
            packets.append(packet[index:index + size])
            index += size
        return packets

    def convert_to_ascii(self, bytes_seq):
        return ''.join(chr(b) for b in bytes_seq)

    def send_tcp_command(self):
        ip = config.ip_entry.get()
        port = config.port_entry.get()
        command = self.code_text.get("1.0", tk.END).strip()
        if not ip or not port or not command:
            print("IP, Porta ou Comando não fornecido.")
            return
        try:
            port = int(port)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((ip, port))
                s.listen(1)
                conn, addr = s.accept()
                print('Connection address:', addr)
                print(f"Enviando comando: {command}")
                conn.sendall(bytes.fromhex(command))
                timeout = 5  # Timeout em segundos
                start_time = time.time()
                attempt = 0
                i = 0
                while 1:
                    data = conn.recv(2048)
                    print(f"Resposta recebida: {data.hex()}")
                    hex_bytes = bytes.fromhex(data.hex())
                    for category, actions in boe.comandos.items():
                        for subcategory, details in actions.items():
                            for key, value in details.items():
                                if "ACK" in value:
                                    ack_hex = value["ACK"].replace(" ", "")
                                    try:
                                        ack_bytes = bytes.fromhex(ack_hex)
                                        i = self.process_ack(ack_bytes, hex_bytes)
                                        if i == 1:
                                            break
                                    except ValueError:
                                        pass
                                        # print(f"ACK inválido ignorado: {ack_hex}")
                            if i == 1:
                                break
                        if i == 1:
                            break
                    if i == 1:
                        break
                    if time.time() - start_time > timeout:
                        print("Timeout atingido.")
                        attempt += 1
                        if attempt == 5:
                            self.ack_text.delete("1.0", tk.END)
                            self.ack_text.insert(tk.END, "Erro ao receber ACK!")
                            break
                        print(f"Enviando comando: {command}")
                        conn.sendall(bytes.fromhex(command))
                        start_time = time.time()

                # self.ack_text.delete("1.0", tk.END)
                # self.ack_text.insert(tk.END, data.hex())
        except ValueError as e:
            print(f"Erro de conversão do comando: {e}")
        except socket.error as e:
            print(f"Erro de socket: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def get_data(self):
        global version_rmc, version_fan, ad_1, ad_2
        ip = config.ip_entry.get()
        port = config.port_entry.get()
        if not ip or not port:
            print("IP, Porta ou Comando não fornecido.")
            return
        try:
            port = int(port)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((ip, port))
                s.listen(1)
                conn, addr = s.accept()
                i1, i2, i3 = 0, 0, 0
                timeout = 5  # Timeout em segundos
                start_time = time.time()
                while 1:
                    data = conn.recv(2048)
                    print(f"Resposta recebida: {data.hex()}")
                    result = self.process_hex_data(data)
                    for header, packets in result:
                        if header == "a1a2a3200011":
                            header, lixo, version_rmc = packets
                            print("header:", header.hex())
                            print("version_rmc:", self.convert_to_ascii(version_rmc))
                            self.version_RMC.config(text=self.convert_to_ascii(version_rmc))
                            i1 = 1
                        elif header == "a1a2a3200013":
                            header, lixo, version_fan = packets
                            print("header:", header.hex())
                            print("version_fan:", self.convert_to_ascii(version_fan))
                            self.version_FAN.config(text=self.convert_to_ascii(version_fan))
                            i2 = 1
                        elif header == "a1a2a31b0014":
                            header, ad_1, lixo, ad_2 = packets
                            print("header:", header.hex())
                            print("ad_1:", self.convert_to_ascii(ad_1))
                            print("ad_2:", self.convert_to_ascii(ad_2))
                            self.version_AD1.config(text=self.convert_to_ascii(ad_1))
                            self.version_AD2.config(text=self.convert_to_ascii(ad_2))
                            i3 = 1
                        print()
                    if i1 == 1 and i2 == 1 and i3 == 1:
                        break
                    if time.time() - start_time > timeout:
                        print("Timeout atingido.")
                        break
                # self.ack_text.delete("1.0", tk.END)
                # self.ack_text.insert(tk.END, data.hex())
        except ValueError as e:
            print(f"Erro de conversão do comando: {e}")
        except socket.error as e:
            print(f"Erro de socket: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    command_interface = CommandInterface(root)
    root.mainloop()


