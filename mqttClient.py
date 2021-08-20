'''
Author: your name
Date: 2021-08-20 10:30:04
LastEditTime: 2021-08-20 10:30:17
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \CoAP-MQTT-brige\mqttClient.py
'''
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
class MqttClient:
    def __init__(self,host,port):
        self.mqttClient = mqtt.Client()
        self.mqttHost = host
        self.mqttPort = port
        self.topic = 'topic'
    def tls_set(self,ca,pem,key):
        self.mqttClient.tls_set(ca, pem, key)
    def on_message(self,client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
    def connect(self,keepalive = 60,properties = None):
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_message = self.on_message
        self.mqttClient.connect(self.mqttHost,self.mqttPort,keepalive,properties = properties)
    def subscribe(self,topic):
        self.topic = topic
    def publish(self,topic, payload=None, qos=0, retain=False, properties=None):
        self.mqttClient.publish(topic, payload, qos, retain, properties)
    def loop_forever(self):
        self.mqttClient.loop_forever()

    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.mqttClient.subscribe(self.topic)