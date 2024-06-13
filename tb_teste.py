import paho.mqtt.client as mqtt
import json
import time

# Configurações do servidor Thingsboard
THINGSBOARD_HOST = "thingsboard.eletromidia.com.br"
THINGSBOARD_PORT = 1883
ACCESS_TOKEN = "dY2YY49K6zFqVV3w8IAR"

# Tópico MQTT onde os dados serão publicados
topic = "v1/devices/me/telemetry"

# Função para conexão bem-sucedida com o servidor Thingsboard
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao Thingsboard com sucesso!")
    else:
        print("Falha na conexão com o Thingsboard. Código de retorno:", rc)

# Função para lidar com mensagens de confirmação de publicação
def on_publish(client, userdata, mid):
    print("Mensagem publicada com sucesso!")

# Configuração do cliente MQTT
client = mqtt.Client()

# Configurações de callbacks
client.on_connect = on_connect
client.on_publish = on_publish

# Conexão com o servidor Thingsboard
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, THINGSBOARD_PORT, keepalive=60)

# Dados a serem enviados
data = {
    "temperature": 900,
    "humidity": 1000
}

# Loop para enviar dados periodicamente (aqui, enviando uma vez apenas)
client.loop_start()
client.publish(topic, json.dumps(data))
time.sleep(1)
client.loop_stop()
client.disconnect()
