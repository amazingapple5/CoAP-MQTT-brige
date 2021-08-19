'''
Author: your name
Date: 2021-08-17 11:05:00
LastEditTime: 2021-08-19 11:31:59
LastEditors: Please set LastEditors
Description: 
iot设备中运行的程序，假设为一台空调，需要满足以下功能：
-传递温度
-远程控制开关机和温度
FilePath: \coapTest\device.py
'''
from coapserver import server
import time
import threading
from coapthon.client.helperclient import HelperClient
from coapserver import AdvancedResource,CoAPServer

class DeviceClient:
    def __init__(self,addr = '127.0.0.1',port = 5683):
        self.addr = addr
        self.port = port
        self.loopThreads = list()
    def setSocket(self,addr,port):
        self.addr=addr
        self.port=port
    def connectServer(self):
        self.coapClient = HelperClient(server=(self.addr, self.port))
    def put(self,uri,payload):
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
            while True and uri in self.loopThreads:
                self.put(uri,payload)
                time.sleep(loopTime)
        
        self.loopThreads.append(uri)
        threading.Thread(name=uri,target=helper).start()
    def stopLoop(self,uri):
        for t in self.loopThreads:
            if t == uri:
                self.loopThreads.remove(t)

    def disconnect(self):
        self.coapClient.stop()

class DevicServer:
    def __init__(self,addr='127.0.0.1',port = 5683):
        self.deviceResource = AdvancedResource('DevicServer')
        #overwriter
        self.deviceResource.onGet = self.onGet
        self.deviceResource.onPut = self.onPut
        self.deviceResource.onPost = self.onPost
        self.deviceResource.onDelete = self.onDelete
        self.addr = addr
        self.port = port
        self.server = None
    def setServer(self):
        self.server = CoAPServer(self.addr,self.port)
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
    def setOnGet(self,func):
        self.deviceResource.onGet = func
    def setOnPut(self,func):
        self.deviceResource.onPut = func
    def setOnPost(self,func):
        self.deviceResource.onPost = func
    def setOnDelete(self,func):
        self.deviceResource.onDelete = func
    def onGet(self,request):
        pass
    def onPut(self,request):
        print(request.uri_path,request.payload)
    def onPost(self,request):
        print(request.uri_path,request.payload)
    def onDelete(self,request):
        pass

if __name__=='__main__':

    c = DeviceClient()
    c.connectServer()
    c.putLoop('Temperature', '27', 5)


    s = DevicServer(port = 5684)
    s.setServer()
    s.add_resource('Temperature')
    s.serverStart()