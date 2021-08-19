'''
Author: your name
Date: 2021-08-16 14:47:17
LastEditTime: 2021-08-17 13:51:42
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \MQTT\coapTest\gateway.py
'''

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from coapthon.client.helperclient import HelperClient
import threading
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.messages.response import Response
from coapthon import defines
client = mqtt.Client()

class AdvancedResource(Resource):
    def __init__(self, name="Advanced"):
        super(AdvancedResource, self).__init__(name)
        self.payload = "Advanced resource"
    
    def render_GET_advanced(self, request, response):
        response.payload = self.payload
        response.max_age = 20
        response.code = defines.Codes.CONTENT.number
        return self, response

    def render_POST_advanced(self, request, response):
        print(request.payload)
        self.payload = request.payload
        assert(isinstance(response, Response))
        response.payload = "Response changed through POST"
        response.code = defines.Codes.CREATED.number
        return self, response

    def render_PUT_advanced(self, request, response):
        print(request.uri_path,request.payload)
        client.publish(request.uri_path,request.payload)
        self.payload = request.payload
        assert(isinstance(response, Response))
        response.payload = "Response changed through PUT"
        response.code = defines.Codes.CHANGED.number
        return self, response

    def render_DELETE_advanced(self, request, response):
        response.payload = "Response deleted"
        response.code = defines.Codes.DELETED.number
        return True, response

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self,(host, port))
        self.add_resource('Temperature', AdvancedResource())
        self.add_resource('TemperatureController', AdvancedResource())
        
def server(Host,Port):
    print("CoAPServer IP addr : %s port : %d "%(Host,Port))
    server = CoAPServer(Host,Port)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('TemperatureController')
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    coapClient = HelperClient(server=("127.0.0.1", 5683))  #coap传递到的服务端的ip和端口
    response = coapClient.put(msg.topic,str(msg.payload))


client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.11.130", 1883, 60)     #mqtt代理所在的ip和端口
threading.Thread(target = server,args=("127.0.0.1", 5684)).start()    #本程序所打开的coap服务端的ip和端口
threading.Thread(target = client.loop_forever()).start()


