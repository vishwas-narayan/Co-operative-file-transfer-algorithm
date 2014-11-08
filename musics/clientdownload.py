import json
import tempfile
from twisted.internet import reactor, protocol
import requests
import logging as LOGI
from BlockCreater import DS, BlockCreater
class EchoClient(protocol.Protocol):
    def __init__(self,id=None):
        self.id=id;
    processId=0
    def connectionMade(self):
        variable=raw_input("enter filename: ")
        self.transport.write(BlockCreater().createInit())
    def dataReceived(self,data):
        print type(data)
        self.transport.write("GET " +str(variable))

        print "contents inside the file %s" %(data)
        f=open("newfile.txt",'a')     
        try:
            d=json.loads(data)
            print type(d)
          
            f.write(d[DS.CONTENT])   
            print "Data received: %s" %(str(data))
            f.close()         
        except:
            print "Error in converting from json"
        self.transport.loseConnection()
class EchoFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed......"
        reactor.stop()
    def clientConnectionLost(self, connector, reason):
        print "Connection lost......"
        reactor.stop()
reactor.connectTCP("localhost",8000,EchoFactory())
reactor.run()   
