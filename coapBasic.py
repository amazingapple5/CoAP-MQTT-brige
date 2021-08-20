'''
Author: lenzo
Date: 2021-08-20 09:23:51
LastEditTime: 2021-08-20 10:10:54
LastEditors: Please set LastEditors
Description: coap客户端、服务端的基本类
FilePath: \CoAP-MQTT-brige\coapBasic.py
'''
import time
import threading
from coapthon.client.helperclient import HelperClient
from coapserver import AdvancedResource,CoAPServer
class CoapbasicClient:
    def __init__(self,addr = '127.0.0.1',port = 5683):
        self.addrClient = addr
        self.portClient = port
        self.clientloopThreads = list()
    def setClientSocket(self,addr,port):
        self.addrClient=addr
        self.portClient=port
    def connectServer(self):
        self.coapClient = HelperClient(server=(self.addrClient, self.portClient))
    def put(self,uri,payload):
        print(uri,payload)
        response = self.coapClient.put(uri,payload)
        return response
    def post(self,uri,payload):
        response = self.coapClient.post(uri,payload)
        return response
    def get(self,uri):
        response = self.coapClient.get(uri)
        return response
    def delete(self,uri):
        response = self.coapClient.delete(uri)
        return response
    def putLoop(self,uri,payload,loopTime):
        def helper():
            while True and uri in self.clientloopThreads:
                self.put(uri,payload)
                time.sleep(loopTime)
        
        self.clientloopThreads.append(uri)
        threading.Thread(name=uri,target=helper).start()
    def stopLoop(self,uri):
        for t in self.clientloopThreads:
            if t == uri:
                self.clientloopThreads.remove(t)

    def disconnect(self):
        self.coapClient.stop()

class CoapBasicServer:
    def __init__(self,addr='127.0.0.1',port = 5683):
        self.deviceResource = AdvancedResource('DevicServer')
        self.addrServer = addr
        self.portServer = port
        self.server = None

    def setServer(self):
        self.deviceResource.onGet = self.onGet
        self.deviceResource.onPut = self.onPut
        self.deviceResource.onPost = self.onPost
        self.deviceResource.onDelete = self.onDelete
        self.server = CoAPServer(self.addrServer,self.portServer)
    def add_resource(self,uri_path):
        if self.server:
            self.server.add_resource(uri_path,self.deviceResource)
    def serverStart(self,listenNumber = 10):
        def helper():
            try:
                self.server.listen(listenNumber)
            except KeyboardInterrupt:
                print("Server Shutdown")
                self.server.close()
                print("Exiting...")
        self.serverThread = threading.Thread(target=helper)
        self.serverThread.start()
    def serverClose(self):
        self.serverThread.setDaemon(True)
        self.server.close()

    def setPayload(self,payload):
        self.deviceResource.payload = payload
    def setSocket(self,addr,port):
        self.addr = addr
        self.port = port
    def onGet(self,request):
        pass
    def onPut(self,request):
        pass
    def onPost(self,request):
        pass
    def onDelete(self,request):
        pass
