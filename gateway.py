'''
Author: lenzo 
Date: 2021-08-19 09:34:37
LastEditTime: 2021-08-20 10:30:34
LastEditors: Please set LastEditors
Description: gateway部分
FilePath: \CoAP-MQTT-brige\gateway.py
'''
import threading

from coapthon.client.helperclient import HelperClient
from coapthon.server.coap import CoAP
from coapBasic import CoapbasicClient,CoapBasicServer
from mqttClient import MqttClient

class Gateway(MqttClient,CoapbasicClient,CoapBasicServer):
    def __init__(self,mqttHost,mqttPort,coapClientHost,coapClientPort,coapServerHost,coapServerPort):
        
        MqttClient.__init__(self, mqttHost, mqttPort)
        CoapbasicClient.__init__(self,coapClientHost,coapClientPort)
        CoapBasicServer.__init__(self,coapServerHost,coapServerPort)

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
    
    
