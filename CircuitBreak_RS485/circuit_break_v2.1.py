import serial
from flask import Flask, jsonify, render_template, request
import threading

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

def read_serial_data(port, baudrate=9600):
    global data
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
                frequency = scale_value(frequency_raw, 10)  # Escalado corretamente para Hz
                voltage = scale_value(voltage_raw, 100)  # Escalado corretamente para V
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
        # Fechar a conexão serial quando o programa for interrompido
        ser.close()
        print("Conexão serial encerrada.")

def send_serial_command(state):
    try:
        ser = serial.Serial('COM12', 115200, timeout=1)
        ser.write(bytes([state]))
        ser.close()
    except serial.SerialException as e:
        print(f"Erro ao enviar comando serial: {e}")

@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/data')
def get_data():
    return jsonify(data)

@app.route('/toggle', methods=['POST'])
def toggle():
    new_state = request.json['state']
    try:
        send_serial_command(new_state)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

def start_serial_thread():
    try:
        serial_thread = threading.Thread(target=read_serial_data, args=('COM12', 115200))  # Altere 'COM11' para a porta correta
        serial_thread.daemon = True
        serial_thread.start()
    except Exception as e:
        print(f"Erro ao iniciar a thread de leitura serial: {e}")

if __name__ == '__main__':
    start_serial_thread()
    app.run(host='0.0.0.0', port=5000, debug=True)
