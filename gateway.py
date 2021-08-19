'''
Author: your name
Date: 2021-08-16 14:47:17
LastEditTime: 2021-08-19 17:24:49
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \MQTT\coapTest\gateway.py
'''
import threading
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from coapthon.client.helperclient import HelperClient
from coapthon.server.coap import CoAP
from device import DeviceClient,DevicServer

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

class Gateway(MqttClient,DeviceClient,DevicServer):
    def __init__(self,mqttHost,mqttPort,coapClientHost,coapClientPort,coapServerHost,coapServerPort):
        
        MqttClient.__init__(self, mqttHost, mqttPort)
        DeviceClient.__init__(self,coapClientHost,coapClientPort)
        DevicServer.__init__(self,coapServerHost,coapServerPort)

    def onPut(self,request):
        self.publish(request.uri_path,request.payload)
    def on_message(self,client, userdata, msg):
        self.put(str(msg.topic),str(msg.payload))
if __name__ == '__main__':
    g = Gateway('192.168.11.130', 1883, '127.0.0.1', 5684, '127.0.0.1', 5683)
    g.connectServer()
    g.setServer()
    g.add_resource('Temperature')
    g.add_resource('TemperatureController')
    g.serverStart()

    g.subscribe("TemperatureController")
    g.connect()
    g.loop_forever()
    
    
