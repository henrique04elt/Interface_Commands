
####################################################################################################    
# Projeto : Circuit Break  RS485                                                                   #
# Autor: H1 and H2                                                                                 #
# Descrição: Projeto para captar os dados de um circuit Break com comunicação RS485 via python,    #
# Craição de uma Servidor FLASK para exibir os dados                                               #
# Versão:3.0 - Dados enviados para um página Flask com botão de abrir e fechar o circuit break     #
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
from flask import Flask, jsonify, render_template, request
import threading
import serial.tools.list_ports

app = Flask(__name__)

# Variáveis globais para armazenar os dados lidos
data = {
    "frequency": 0.0,
    "voltage": 0.0,
    "current": 0.0,
    "power": 0.0,
    "power_factor": 0.0,
    "temperature": 0.0,
    "cb_state": "Unknown"
}

ser = None

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
    global data, ser
    try:
        # Configuração da porta serial
        ser = serial.Serial(port, baudrate, timeout=1)
        
        while True:
            # Ler os dados da porta serial
            serial_data = ser.read(14)  # Ler 14 bytes conforme a estrutura fornecida
            
            if len(serial_data) == 14:
                # Interpretação dos dados
                frequency_raw = int.from_bytes(serial_data[0:2], byteorder='big')
                voltage_raw = int.from_bytes(serial_data[2:4], byteorder='big')
                current_raw = int.from_bytes(serial_data[4:6], byteorder='big')
                power_raw = int.from_bytes(serial_data[6:8], byteorder='big')
                power_factor_raw = int.from_bytes(serial_data[8:10], byteorder='big')
                temperature_raw = int.from_bytes(serial_data[10:12], byteorder='big')
                cb_state = int.from_bytes(serial_data[12:14], byteorder='big')

                # Aplicar escalas apropriadas
                frequency = scale_value(frequency_raw, 100)  # Escalado corretamente para Hz
                voltage = scale_value(voltage_raw, 10)  # Escalado corretamente para V
                current = scale_value(current_raw, 100)  # Assumindo que a escala está correta
                power = scale_value(power_raw, 10)  # Assumindo que a escala está correta
                power_factor = scale_value(power_factor_raw, 1000)  # Assumindo que a escala está correta
                temperature = scale_value(temperature_raw, 10)  # Escalado corretamente para °C

                # Atualizar os dados globais
                data = {
                    "frequency": frequency,
                    "voltage": voltage,
                    "current": current,
                    "power": power,
                    "power_factor": power_factor,
                    "temperature": temperature,
                    "cb_state": circuit_breaker_states.get(cb_state, "Unknown state")
                }
                
    except serial.SerialException as e:
        print(f"Erro na porta serial: {e}")
    except KeyboardInterrupt:
        print("Leitura serial interrompida pelo usuário.")
    finally:
        if ser is not None:
            ser.close()
            print("Conexão serial encerrada.")

def find_available_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        try:
            s = serial.Serial(port.device)
            s.close()
            return port.device
        except (OSError, serial.SerialException):
            pass
    return None

# Rota para exibir os dados na página web
@app.route('/')
def index():
    return render_template('index.html', data=data)

# Rota para retornar os dados em formato JSON
@app.route('/data')
def get_data():
    return jsonify(data)

# Rota para enviar comando de ligar/desligar
@app.route('/control', methods=['POST'])
def control_cb():
    global ser
    action = request.json.get('action')
    if action == "on":
        command = b'\x01'
    elif action == "off":
        command = b'\x02'
    else:
        return jsonify({"status": "invalid action"}), 400

    if ser is not None and ser.is_open:
        ser.write(command)
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "serial not connected"}), 500

# Função para iniciar a leitura serial em uma thread separada
def start_serial_thread():
    port = find_available_port()
    if port:
        try:
            serial_thread = threading.Thread(target=read_serial_data, args=(port, 115200))
            serial_thread.daemon = True
            serial_thread.start()
            print(f"Lendo dados da porta {port}")
        except Exception as e:
            print(f"Erro ao iniciar a thread de leitura serial: {e}")
    else:
        print("Nenhuma porta serial disponível foi encontrada.")

if __name__ == '__main__':
    start_serial_thread()
    app.run(host='0.0.0.0', port=5000, debug=True)
