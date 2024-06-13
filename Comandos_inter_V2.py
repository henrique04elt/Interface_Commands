import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import boe

class CommandInterface:
    def __init__(self, master):
        self.master = master
        master.title("BOE Command Interface")
        master.geometry("800x600")  # Definindo o tamanho inicial da janela

        self.style = ttk.Style()
        self.style.theme_use("clam")  # Escolha do tema (pode ser alterado)

        # Estilo personalizado
        self.style.configure("TLabelFrame", background="#f7f7f7", font=("Helvetica", 14), relief="solid", borderwidth=1)
        self.style.configure("TButton", background="#808080", foreground="white", font=("Helvetica", 12), padding=5)
        self.style.configure("TCombobox", font=("Helvetica", 12))
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("TText", font=("Helvetica", 12), wrap="word")

        # Estilo específico para botões de configuração e leitura
        self.style.configure("Setting.TButton", background="#C0C0C0", foreground="black")
        self.style.configure("Reading.TButton", background="#C0C0C0", foreground="black")

        # Estilo para bordas arredondadas
        self.style.configure("Rounded.TFrame", background="#f7f7f7", relief="solid", borderwidth=1)
        self.style.map("Rounded.TFrame",
                       background=[("active", "#e0e0e0")])

        # Carrega a imagem do logo
        logo_image = Image.open("Eletromidia_logo.png")
        logo_image = logo_image.resize((100, 100))
        self.logo = ImageTk.PhotoImage(logo_image)

        # Exibe o logo no canto superior esquerdo
        self.logo_label = ttk.Label(master, image=self.logo)
        self.logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.label_frame = ttk.LabelFrame(master, text='Commands', padding=10, style="Rounded.TFrame")
        self.label_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.command_type_label = ttk.Label(master, text="Command Type: None", font=("Helvetica", 14))
        self.command_type_label.grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")

        self.show_setting_button = ttk.Button(self.label_frame, text="Configuration Commands", style="Setting.TButton", command=self.show_setting_commands)
        self.show_setting_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.show_reading_button = ttk.Button(self.label_frame, text="Reading Commands", style="Reading.TButton", command=self.show_reading_commands)
        self.show_reading_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.command_variable = tk.StringVar(master)
        self.command_variable.set('Select a command')

        self.command_menu = ttk.Combobox(self.label_frame, textvariable=self.command_variable, state='readonly', width=40)
        self.command_menu.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky='ew')
        self.command_menu.bind('<<ComboboxSelected>>', self.update_display)

        self.code_frame = ttk.LabelFrame(master, text="Code", padding=10, style="Rounded.TFrame")
        self.code_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        self.code_text = tk.Text(self.code_frame, height=5, width=50, font=("Helvetica", 12), bg="#f0f0f0", relief="solid", borderwidth=1)
        self.code_text.pack(fill=tk.BOTH, expand=True)

        self.ack_frame = ttk.LabelFrame(master, text="ACK", padding=10, style="Rounded.TFrame")
        self.ack_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        self.ack_text = tk.Text(self.ack_frame, height=5, width=50, font=("Helvetica", 12), bg="#f0f0f0", relief="solid", borderwidth=1)
        self.ack_text.pack(fill=tk.BOTH, expand=True)

        self.relay_frame = ttk.LabelFrame(master, text="Relay Control", padding=10, style="Rounded.TFrame")
        self.relay_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ne")


        self.create_relay_buttons()
        self.relay_status = {i: "OFF" for i in range(6)}  # Inicialmente, todos os relés estão desligados


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

        self.ack_text.delete("1.0", tk.END)
        self.ack_text.insert(tk.END, ack)

    def show_setting_commands(self):
        self.command_type_label.config(text="Command Type: Setting")
        self.populate_commands('Setting')

    def show_reading_commands(self):
        self.command_type_label.config(text="Command Type: Reading")
        self.populate_commands('Reading')

    def populate_commands(self, command_type):
        self.code_text.delete("1.0", tk.END)  # Limpa o texto do código
        self.ack_text.delete("1.0", tk.END)   # Limpa o texto do ACK

        commands_list = []
        for category, commands in boe.comandos.items():
            if command_type in commands:
                for command in commands[command_type]:
                    commands_list.append(f"{category} - {command}")
        self.command_menu['values'] = commands_list
        if not commands_list:
            self.command_variable.set('No commands found')
        else:
            self.command_variable.set('Select a command')

    def update_display(self, event):
        selected_command = self.command_variable.get()
        if ' - ' not in selected_command:
            return  # Do nothing if selection is invalid

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

        self.ack_text.delete("1.0", tk.END)
        self.ack_text.insert(tk.END, ack)


if __name__ == "__main__":
    root = tk.Tk()
    command_interface = CommandInterface(root)
    root.mainloop()
