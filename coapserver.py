'''
Author: lenzo
Date: 2021-08-19 09:34:37
LastEditTime: 2021-08-20 10:20:17
LastEditors: Please set LastEditors
Description: coap服务端的基础类
FilePath: \CoAP-MQTT-brige\coapserver.py
'''
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.messages.response import Response
from coapthon import defines
Host = "127.0.0.1"  		
Port = 5684             

class AdvancedResource(Resource):
    def __init__(self, name="Advanced"):
        super(AdvancedResource, self).__init__(name)
        self.payload = "Advanced resource"
    def render_GET_advanced(self, request, response):
        response.payload = self.payload
        response.max_age = 20
        response.code = defines.Codes.CONTENT.number
        self.onGet(request)
        return self, response

    def render_POST_advanced(self, request, response):
        res = AdvancedResource()
        res.location_query = request.uri_query
        res.payload = request.payload
        assert(isinstance(response, Response))
        response.payload = "Response changed through POST"
        response.code = defines.Codes.CREATED.number
        self.onPost(request)
        return res, response

    def render_PUT_advanced(self, request, response):
        print(request.payload)
        self.payload = request.payload
        assert(isinstance(response, Response))
        response.payload = "Response changed through PUT"
        response.code = defines.Codes.CHANGED.number
        self.onPut(request)
        return self, response

    def render_DELETE_advanced(self, request, response):
        response.payload = "Response deleted"
        response.code = defines.Codes.DELETED.number
        self.onDelete(request)
        return True, response
    def onGet(self,request):
        pass
    def onPut(self,request):
        print(request.uri_path,request.payload)
    def onPost(self,request):
        pass
    def onDelete(self,request):
        pass

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self,(host, port))
        #self.add_resource('Temperature', AdvancedResource())
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

if __name__ == '__main__':
    server(Host,Port)
