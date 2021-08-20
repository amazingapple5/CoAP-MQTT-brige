'''
Author: your name
Date: 2021-08-17 11:05:00
LastEditTime: 2021-08-20 09:27:34
LastEditors: Please set LastEditors
Description: 
FilePath: \coapTest\device.py
'''
from coapserver import server
from coapBasic import CoapBasicServer,CoapbasicClient

class Device(CoapbasicClient,CoapBasicServer):
    def __init__(self,serverAddr='127.0.0.1',serverPort = 5683,clientAddr = '127.0.0.1',clientPort = 5683):
        CoapbasicClient.__init__(self,clientAddr,clientPort)
        CoapBasicServer.__init__(self,serverAddr,serverPort)

if __name__=='__main__':

    d = Device(serverPort=5684)
    d.connectServer()
    d.putLoop('Temperature', '27', 5)

    d.setServer()
    d.add_resource('Temperature')
    d.serverStart()