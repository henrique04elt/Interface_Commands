####################################################################################################    
# Projeto : Circuit Break  RS485                                                                   #
# Autor: H1 and H2                                                                                 #
# Descrição: Projeto para captar os dados de um circuit Break com comunicação RS485 via python,    #
# Craição de uma Servidor FLASK para exibir os dados                                               #
# Versão : V1.0                                                                                    #
# Estrutura dos dados enviados pelo FTDI                                                           #
# 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00               #
# Frequencia |Tensão     | Corrente  | Potencia  | FP        |Temperatura| Estado                  #
# 2 bytes - Frequencia, 2 bytes - Tensão, 2 bytes - Corrente, 2 bytes - Potenencia,                #        
# 2 bytes - Fator de Potencia (FP),                                                                #
# 2 bytes - Temperatura, 2 bytes - Estado do Circuit Breaker (CB)                                  #
####################################################################################################
# Estados do Circuit Break                                                                         #                                                                                                   
#  0:Manual switching                                                                              #
#  1:Command switchin                                                                              #
#  2:Fault switching                                                                               #
#  3:Power off switching                                                                           #
#  4:Manual closing                                                                                #
#  5:Command closing                                                                               #
#  6:Automatic closing                                                                             #
#  7:Command lock (Need to be unlocked before closing)                                             #
#  8:Failure lock (need to be unlocked before closing)                                             #
#  9:Mechanism padlock                                                                             #
#  10:Timing switching                                                                             #
#  11:Timing closing                                                                               #
#  12:Leakage switching                                                                            #
####################################################################################################

import serial

# Mapeamento dos estados do Circuit Breaker
circuit_breaker_states = {
    0: "Manual switching",
    1: "Command switching",
    2: "Fault switching",
    3: "Power off switching",
    4: "Manual closing",
    5: "Command closing",
    6: "Automatic closing",
    7: "Command lock (Need to be unlocked before closing)",
    8: "Failure lock (need to be unlocked before closing)",
    9: "Mechanism padlock",
    10: "Timing switching",
    11: "Timing closing",
    12: "Leakage switching"
}

def scale_value(raw_value, scale_factor):
    return raw_value / scale_factor

def read_serial_data(port, baudrate=115200):
    # Configuração da porta serial
    ser = serial.Serial(port, baudrate, timeout=1)
    
    try:
        while True:
            # Ler os dados da porta serial
            data = ser.read(14)  # Ler 14 bytes conforme a estrutura fornecida
            
            if len(data) == 14:
                # Interpretação dos dados
                frequency_raw = int.from_bytes(data[0:2], byteorder='big')
                voltage_raw = int.from_bytes(data[2:4], byteorder='big')
                current_raw = int.from_bytes(data[4:6], byteorder='big')
                power_raw = int.from_bytes(data[6:8], byteorder='big')
                power_factor_raw = int.from_bytes(data[8:10], byteorder='big')
                temperature_raw = int.from_bytes(data[10:12], byteorder='big')
                cb_state = int.from_bytes(data[12:14], byteorder='big')

                # Aplicar escalas apropriadas
                frequency = scale_value(frequency_raw, 100)  # Escalado corretamente para Hz
                voltage = scale_value(voltage_raw, 10)  # Escalado corretamente para V
                current = scale_value(current_raw, 100)  # Assumindo que a escala está correta
                power = scale_value(power_raw, 10)  # Assumindo que a escala está correta
                power_factor = scale_value(power_factor_raw, 1000)  # Assumindo que a escala está correta
                temperature = scale_value(temperature_raw, 10)  # Escalado corretamente para °C

                # Mapear o estado do Circuit Breaker
                cb_state_description = circuit_breaker_states.get(cb_state, "Unknown state")

                # Imprimir os dados interpretados
                print(f"Frequencia: {frequency} Hz")
                print(f"Tensão: {voltage} V")
                print(f"Corrente: {current} A")
                print(f"Potência: {power} W")
                print(f"Fator de Potência: {power_factor}")
                print(f"Temperatura: {temperature} °C")
                print(f"Estado do Circuit Breaker: {cb_state_description}")
                print("-" + "-"*40)
                
    except KeyboardInterrupt:
        # Fechar a conexão serial quando o programa for interrompido
        ser.close()
        print("Conexão serial encerrada.")

# Substitua 'COM3' pelo número da porta serial que está utilizando
read_serial_data('COM13')
