# import imp
# from random import random
import threading
import time
import random
import paho.mqtt.client as paho
import numpy as np

broker = '5g-vue.projects.uom.lk'
port = 1883
username = 'iot_user'
password = 'iot@1234'
client_id = 'group_07m'

topic = "/group_07m"
temp_topic = topic + "/temp01"

sensors = ['Gas_01','Smoke_01','Smoke_02','Security_01','Security_02','Temp_01','Temp_02','Humidity_01','Motion_01','Power_01']

sensor_intervals = [25,20,20,20,25,30,25,40,25,35]

prev_reading = ['n','n','n','n','n','n','n','n','n','n']

is_periodical_values = [0,0,0,1,1,0,0,0,1,0]
threshold_values = [0.3,0.3,0.3,0.75,0.75,0.3,0.3,0.3,0.1,0.3]
min_values = [10,20,20,0,0,15,-10,0,0,0]
max_values = [5000,6000,6000,0,0,45,30,100,0,400]
avg_values = [400,500,500,0,0,28,17,50,0,35]
a_values = [1,3,3,0,0,0.2,0.2,0.2,0,0.2]
b_values = [0.0004,0.0005,0.0005,0,0,0.2,0.2,0.2,0,0.6]
c_values = [0.0005,0.006,0.0006,0,0,0.2,0.1,0.2,0,0.5]

def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =", str(message.payload.decode("utf-8")))


def sensor_readings(is_periodical,sensor_no,threshold,min_val,avg_val,max_val,a,b,c):
    if is_periodical:
        weight_1,weight_2,weight_3 = np.random.rand(3)
        prev_val = 0
        if prev_reading[sensor_no] != 'n':
            prev_val = prev_reading[sensor_no]
        reading =prev_val + b*(max_val-prev_val)*weight_1 +c*(avg_val-prev_val)*weight_3 -a*(prev_val-min_val)*weight_2
        reading = min(max(min_val,reading),max_val)
        prev_reading[sensor_no] = reading
        reading = round(reading,3)
        return reading
    else:
        return int(random.uniform(0,1)<threshold)
        

def publish_function(name,seed, cycles,sensor_val):
    current_topic = topic +"/"+ sensors[sensor_val]
    for cyc in range(cycles):
        print(current_topic+" is publishing")
        current_reading = sensor_readings(is_periodical_values[sensor_val],sensor_val,threshold_values[sensor_val],min_values[sensor_val],avg_values[sensor_val],max_values[sensor_val],a_values[sensor_val],b_values[sensor_val],c_values[sensor_val])
        client.publish(current_topic,current_reading)
        time.sleep(sensor_intervals[sensor_val])

# # configure mqtt client
# client = paho.Client(client_id)
# client.username_pw_set(username, password)
# client.on_message = on_message

# print("connecting to broker ", broker)
# client.connect(broker)

# client.loop_start()  # start loop to process received messages
# # client.loop_forever()
# print("subscribing ")
# client.subscribe(temp_topic)  # subscribe

# val = 30
# val_temp = val
# rng = np.random.default_rng(3)

# while(1):
#     print("publishing ")
#     rand_num = rng.integers(low=-3, high=8, size=1)
#     print(round(rand_num[0], 2))
#     val_temp = val_temp+rand_num[0]
#     val = 0.8*val + 0.2*val_temp
#     if(val < 0):
#         val = 0
#     client.publish(temp_topic, val)  # publish
#     time.sleep(10)
# client.disconnect()  # disconnect

if __name__ == "__main__":
    # configure mqtt client
    client = paho.Client(client_id)
    client.username_pw_set(username, password)
    client.on_message = on_message

    print("connecting to broker ", broker)
    client.connect(broker)

    threads = []

    for t in range(1,11):
        # threads.append(threading.Thread(target=publish_function(sensor_val=t-1,cycles=1),args=(t,t,10))) 
        # threads.append(threading.Thread(target=publish_function,args=(t,t,10),kwargs = {'sensor_val' : t})) 
        threads = threading.Thread(target=publish_function,args=(t,t,10,t-1))
        threads.start() 
    
    