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
import boe

def criar_janela_info():
    med = tk.Tk()
    med.title("Medições V1.0")

    style = ttk.Style()
    style.theme_use("clam")
    style.map("Rounded.TFrame", background=[("active", "#e0e0e0")])

    Voltage = ttk.Label(med, text="Tensão: ", width=15)
    Voltage.grid(row=0, column=0, padx=10, pady=2, sticky="e")
    Voltage = ttk.Label(med, text=config.voltage, width=15)
    Voltage.grid(row=0, column=1, padx=0, pady=2, sticky="w")

    Current = ttk.Label(med, text="Corrente: ", width=15)
    Current.grid(row=1, column=0, padx=10, pady=2, sticky="e")
    Current = ttk.Label(med, text=config.current, width=15)
    Current.grid(row=1, column=1, padx=0, pady=2, sticky="w")

    Freq = ttk.Label(med, text="Frequencia: ", width=15)
    Freq.grid(row=2, column=0, padx=10, pady=2, sticky="e")
    Freq = ttk.Label(med, text=config.frequencia, width=15)
    Freq.grid(row=2, column=1, padx=0, pady=2, sticky="w")

    energy = ttk.Label(med, text="Consumo: ", width=15)
    energy.grid(row=3, column=0, padx=10, pady=2, sticky="e")
    energy = ttk.Label(med, text=config.energy, width=15)
    energy.grid(row=3, column=1, padx=0, pady=2, sticky="w")

    potencia_efetiva = ttk.Label(med, text="potencia_efetiva: ", width=15)
    potencia_efetiva.grid(row=4, column=0, padx=10, pady=2, sticky="e")
    potencia_efetiva = ttk.Label(med, text=config.potencia_efetiva, width=15)
    potencia_efetiva.grid(row=4, column=1, padx=0, pady=2, sticky="w")

    potencia_reativa = ttk.Label(med, text="potencia_reativa: ", width=15)
    potencia_reativa.grid(row=5, column=0, padx=10, pady=2, sticky="e")
    potencia_reativa = ttk.Label(med, text=config.potencia_reativa, width=15)
    potencia_reativa.grid(row=5, column=1, padx=0, pady=2, sticky="w")

    V12_1 = ttk.Label(med, text="V12_1: ", width=15)
    V12_1.grid(row=6, column=0, padx=10, pady=2, sticky="e")
    V12_1 = ttk.Label(med, text=config.v12_1, width=15)
    V12_1.grid(row=6, column=1, padx=0, pady=2, sticky="w")

    V12_2 = ttk.Label(med, text="V12_2: ", width=15)
    V12_2.grid(row=7, column=0, padx=10, pady=2, sticky="e")
    V12_2 = ttk.Label(med, text=config.v12_2, width=15)
    V12_2.grid(row=7, column=1, padx=0, pady=2, sticky="w")

    V24 = ttk.Label(med, text="V24: ", width=15)
    V24.grid(row=8, column=0, padx=10, pady=2, sticky="e")
    V24 = ttk.Label(med, text=config.v24, width=15)
    V24.grid(row=8, column=1, padx=0, pady=2, sticky="w")

    med.mainloop()

if __name__ == "__main__":
    criar_janela_info()