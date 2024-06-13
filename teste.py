import tkinter as tk
from tkinter import ttk

class ScheduleInterface:
    def __init__(self, master, command_interface):
        self.master = master
        self.command_interface = command_interface  # Referência para a interface principal
        master.title("Schedule Interface")

        # Botão para voltar à interface principal
        self.back_button = ttk.Button(master, text="Voltar", command=self.close_schedule_interface)
        self.back_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    def close_schedule_interface(self):
        # Método para fechar a interface do programa Schedule e retornar à interface principal
        self.master.destroy()  # Fecha a interface do programa Schedule
        self.command_interface.master.deiconify()  # Mostra a interface principal novamente

class CommandInterface:
    def __init__(self, master):
        self.master = master
        master.title("Command Interface")

        # Botão para abrir a interface do programa Schedule
        self.schedule_button = ttk.Button(master, text="Abrir Schedule", command=self.open_schedule_interface)
        self.schedule_button.pack(pady=20)

    def open_schedule_interface(self):
        # Método para abrir a interface do programa Schedule e esconder a interface principal
        self.master.withdraw()  # Esconde a interface principal
        schedule_window = tk.Toplevel(self.master)
        ScheduleInterface(schedule_window, self)  # Passa a referência da interface principal

if __name__ == "__main__":
    root = tk.Tk()
    command_interface = CommandInterface(root)
    root.mainloop()
