from flask import Flask, render_template, request
import socket

app = Flask(__name__)


# Função para enviar dados para a porta 44406
def send_data(data):
    UDP_IP = "127.0.0.1"  # Endereço IP do servidor
    UDP_PORT = 44406  # Porta para enviar os dados

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data.encode(), (UDP_IP, UDP_PORT))
    sock.close()


# Rota para a página principal
@app.route('/')
def index():
    return render_template('index.html')


# Rota para receber os dados do formulário e enviar para a porta 44406
@app.route('/send_data', methods=['POST'])
def send_data_route():
    rmc = request.form['rmc']
    ad = request.form['ad']
    moden = request.form['moden']
    ad2 = request.form['ad2']

    # Concatenando os dados para envio
    data = f"RMC: {rmc}, AD: {ad}, MODEN: {moden}, AD2: {ad2}"

    send_data(data)
    return 'Dados enviados com sucesso para o ESP32!'


if __name__ == '__main__':
    app.run(debug=True)
