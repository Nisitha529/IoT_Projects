import time
import paho.mqtt.client as paho
import numpy as np

broker = '5g-vue.projects.uom.lk'
port = 1883
topic = "/group_id"
client_id = 'python-mqtt'
username = 'iot_user'
password = 'iot@1234'


temp_topic = topic + "/temp01"


def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =", str(message.payload.decode("utf-8")))


# configure mqtt client
client = paho.Client(client_id)
client.username_pw_set(username, password)
client.on_message = on_message

print("connecting to broker ", broker)
client.connect(broker)

client.loop_start()  # start loop to process received messages
# client.loop_forever()
print("subscribing ")
client.subscribe(temp_topic)  # subscribe

val = 30
rng = np.random.default_rng(3)

while(1):
    print("publishing ")
    rand_num = rng.integers(low=-5, high=5, size=1)
    val = 0.8*val + 0.2*rand_num[0]
    if(val < 0):
        val = 0
    client.publish(temp_topic, val)  # publish
    time.sleep(5)
client.disconnect()  # disconnect