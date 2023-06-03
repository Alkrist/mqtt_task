import paho.mqtt.client as paho
import sys
import ssl
import logging
import json
from datetime import datetime

# Cesta k souboru logu a nastavení loggera
LOG_PATH = "C:\\Users\\Alkrist.MSI\\Documents\\Work\\python\\test_task\\logs\\django-sub.log"
logging.basicConfig(filename=LOG_PATH, encoding='utf-8', level=logging.INFO)

# Výpis správ do logu


def log_infomessage(message: str):
    now = datetime.now()
    logging.info(now.strftime("%d/%m/%Y %H:%M:%S")+" "+message)

# Chybové hlašení do logu


def log_errormessage(message: str):
    now = datetime.now()
    logging.critical(now.strftime("%d/%m/%Y %H:%M:%S")+" "+message)


log_infomessage("started")

# Listener na přijetí zpráv od brokera a jejich uložení do databáze
# TODO: add value fields instead of JSON field


def onMessage(client, userdata, msg):
    from .models import Coin
    str_data = msg.payload.decode()
    insert(str_data)
    log_infomessage("Message received on topic: " +
                    msg.topic + "\nMessage: " + str_data)



def insert(str_data):
    from .models import Coin
    jd = json.loads(str_data)
    '''if (Coin.objects.get(id=jd['id']) is not None):
        Coin.objects.get(id=jd['id']).rank = jd['rank']
        Coin.objects.get(id=jd['id']).symbol = jd['symbol']
        Coin.objects.get(id=jd['id']).name = jd['name']
        Coin.objects.get(id=jd['id']).supply = jd['supply']
    else:'''
    i = Coin(identifier=jd['id'], rank=jd['rank'], symbol=jd['symbol'], name=jd['name'], supply=jd['supply'])
    i.save()

# Data pro prihlášení na mqtt broker
USERNAME = "user1"
PASSWORD = "321"
TOPIC = "test/crypto"

# Cesty k souborům certifikátu
CA_PATH = "C:/Users/Alkrist.MSI/Documents/Work/python/test_task/ssl_certificate/ca.crt"
CLIENT_CERT_PATH = "C:/Users/Alkrist.MSI/Documents/Work/python/test_task/ssl_certificate/client.crt"
CLIENT_KEY_PATH = "C:/Users/Alkrist.MSI/Documents/Work/python/test_task/ssl_certificate/client.key"

# Vytvoření klienta a napojení klienta na brokera, nastavení listenera
client = paho.Client()
client.on_message = onMessage

# Specifikace certifikátu a nastavení TLS (TLS se nepoužívá, používá se SSL)
client.tls_set(CA_PATH, CLIENT_CERT_PATH, CLIENT_KEY_PATH,
               tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(True)

# Specifikace loginu a hesla
client.username_pw_set(USERNAME, password=PASSWORD)

# Připojení klienta na port 8883 (SSL)
if client.connect("localhost", 8883, 60) != 0:
    print("Could not connect to MQTT broker!")
    log_errormessage("Could not connect to MQTT broker! Stopping client...")
    sys.exit(-1)
else:
    log_infomessage("Subscriber client has connected to broker.")

client.subscribe(TOPIC)
