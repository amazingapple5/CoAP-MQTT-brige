'''
Author: your name
Date: 2021-08-12 16:31:05
LastEditTime: 2021-08-19 16:49:26
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \coapTestDemo.py
'''
import time
from coapthon.client.helperclient import HelperClient
from coapthon.messages.response import Response
host = "127.0.0.1"
port = 5684
path = "basic"
def client(host,port):
    client = HelperClient(server=(host, port))
    while True :
        op = input()
        if op=='put':
            path = input()
            payload = input()
            response = client.put(path,payload)
            print(response.payload)
            print('==================put end====================')
        elif op == 'post':
            path = input()
            payload = input()
            response = client.post(path,payload)
            response.pretty_print()
            print('==================post end====================')
        elif op == 'get':
            path = input()
            response = client.get(path)
            print(response.payload)
            print('==================get end====================')
        elif op=='delete':
            path = input()
            response = client.delete(path)
            print(response.payload)
            print('==================delete end====================')
        elif op=='quit':
            break
    client.stop()

if __name__ == '__main__':
    client(host, port)

