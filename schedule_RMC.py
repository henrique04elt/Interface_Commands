## Programa para geração de código para Schedule de Brilho ##
## Henrique Rosa                                           ##
## Data : 20/04/2024                                       ##
## Schedule_RMC_v1                                         ##

import tkinter as tk
from datetime import datetime, time

def obter_valor_hex(valor):
    if isinstance(valor, int):
        return format(valor, '02x')
    elif isinstance(valor, str) and valor.startswith('0x'):
        return valor
    else:
        return format(int(valor), '02x')

def criar_comando_schedule():
    global campo_comando

    programacao = obter_valores_inseridos()

    if programacao is not None:
        comando = "ff 55 10 23"  ## Valor não muda

        for horario, percentagem in programacao:
            comando += f" {obter_valor_hex(horario.hour)} {obter_valor_hex(horario.minute)} {obter_valor_hex(percentagem)}"

        checksum = obter_checksum(comando)
        comando += f" {checksum}"

        campo_comando.config(state=tk.NORMAL)
        campo_comando.delete(1.0, tk.END)
        campo_comando.insert(tk.END, comando)
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
    janela.title("Configuração da Schedule")

    horarios_entries = []
    percentagens_entries = []

    for i in range(5):
        tk.Label(janela, text=f"{i+1}º horário:").grid(row=i, column=0, padx=5, pady=5)
        horario_entry = tk.Entry(janela)
        horario_entry.grid(row=i, column=1, padx=5, pady=5)
        horarios_entries.append(horario_entry)

        tk.Label(janela, text="Porcentagem:").grid(row=i, column=2, padx=5, pady=5)
        percentagem_entry = tk.Entry(janela)
        percentagem_entry.grid(row=i, column=3, padx=5, pady=5)
        percentagens_entries.append(percentagem_entry)

    botao_criar_comando = tk.Button(janela, text="Criar Comando Schedule", command=criar_comando_schedule)
    botao_criar_comando.grid(row=5, columnspan=4, pady=10)

    tk.Label(janela, text="Comando Gerado:").grid(row=6, column=0, padx=5, pady=5)
    campo_comando = tk.Text(janela, height=1, width=80)  # Ajuste a largura conforme necessário
    campo_comando.grid(row=6, column=1, columnspan=3, padx=5, pady=5)
    campo_comando.config(state=tk.DISABLED)

    janela.mainloop()

if __name__ == "__main__":
    criar_janela()
