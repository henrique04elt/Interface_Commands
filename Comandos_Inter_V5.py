import tkinter as tk
from tkinter import ttk
import socket
import threading

class CommandInterface:
    def __init__(self, master):
        self.master = master
        master.title("Command Interface")
        master.geometry("400x200")

        # Criar os widgets
        self.create_widgets()

    def create_widgets(self):
        # Frame para os widgets principais
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Entrada para o endereço IP do servidor
        self.ip_label = ttk.Label(self.main_frame, text="Server IP:")
        self.ip_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ip_entry = ttk.Entry(self.main_frame, width=20)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)

        # Entrada para a porta do servidor
        self.port_label = ttk.Label(self.main_frame, text="Server Port:")
        self.port_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.port_entry = ttk.Entry(self.main_frame, width=10)
        self.port_entry.grid(row=1, column=1, padx=5, pady=5)

        # Botão para enviar o comando
        self.send_button = ttk.Button(self.main_frame, text="Send Command", command=self.send_command)
        self.send_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")

        # Saída para exibir a resposta do servidor
        self.response_label = ttk.Label(self.main_frame, text="Response:")
        self.response_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.response_text = tk.Text(self.main_frame, height=5, width=40)
        self.response_text.grid(row=3, column=1, padx=5, pady=5)

    def send_command(self):
        # Obter o endereço IP e a porta do servidor
        ip = self.ip_entry.get()
        port = self.port_entry.get()

        # Iniciar uma nova thread para operação de rede
        threading.Thread(target=self.send_command_thread, args=(ip, port)).start()

    def send_command_thread(self, ip, port):
        try:
            # Criar o socket e se conectar ao servidor
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, int(port)))

                # Enviar o comando específico
                command = bytes.fromhex('ff 55 04 ad 01 00 00 06')  # Substitua pelo seu comando
                s.sendall(command)  # Envie o comando

                print("Comando enviado:", command)
        except Exception as e:
            # Em caso de erro, exibir uma mensagem de erro
            self.master.after(0, lambda err=str(e): self.show_error(err))

    def show_error(self, error_message):
        self.response_text.insert(tk.END, f"Error: {error_message}\n")

if __name__ == "__main__":
    root = tk.Tk()
    command_interface = CommandInterface(root)
    root.mainloop()
