import tkinter as tk
from tkinter import ttk
import boe

class CommandInterface:
    def __init__(self, master):
        self.master = master
        master.title("BOE Command Interface")

        # Frame para os comandos
        self.command_frame = ttk.LabelFrame(master, text="Commands")
        self.command_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.command_label = ttk.Label(self.command_frame, text="Select Command:")
        self.command_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.command_variable = tk.StringVar(master)
        self.command_variable.set(list(boe.comandos.keys())[0])  # Set the default command
        self.command_menu = ttk.OptionMenu(self.command_frame, self.command_variable, *boe.comandos.keys(), command=self.update_display)
        self.command_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Frame para os códigos e ACKs
        self.code_ack_frame = ttk.LabelFrame(master, text="Code and ACK")
        self.code_ack_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.code_label = ttk.Label(self.code_ack_frame, text="Code:")
        self.code_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.code_text = tk.Text(self.code_ack_frame, height=10, width=50)
        self.code_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.code_scroll = ttk.Scrollbar(self.code_ack_frame, command=self.code_text.yview)
        self.code_scroll.grid(row=1, column=1, sticky="ns")
        self.code_text.config(yscrollcommand=self.code_scroll.set)

        self.ack_label = ttk.Label(self.code_ack_frame, text="ACK:")
        self.ack_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.ack_text = tk.Text(self.code_ack_frame, height=10, width=50)
        self.ack_text.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

        self.ack_scroll = ttk.Scrollbar(self.code_ack_frame, command=self.ack_text.yview)
        self.ack_scroll.grid(row=1, column=3, sticky="ns")
        self.ack_text.config(yscrollcommand=self.ack_scroll.set)

        self.update_display()  # Atualizar exibição inicial

    def update_display(self, *args):
        selected_command = self.command_variable.get()
        command_data = boe.comandos[selected_command]
        self.code_text.delete("1.0", tk.END)  # Limpar código anterior
        self.ack_text.delete("1.0", tk.END)   # Limpar ACK anterior

        for state, state_data in command_data.items():
            self.code_text.insert(tk.END, f"{state}:\n")
            self.ack_text.insert(tk.END, f"{state}:\n")
            for relay, relay_data in state_data.items():
                send_data = relay_data.get('Send Data', 'No data available')
                ack_data = relay_data.get('ACK', 'No ACK available')
                self.code_text.insert(tk.END, f"{relay}:\n{send_data}\n\n")
                self.ack_text.insert(tk.END, f"{relay}:\n{ack_data}\n\n")

    def send_command(self):
        # Implementar envio de comando aqui
        pass

root = tk.Tk()
app = CommandInterface(root)
root.mainloop()
