
"""Requires Twisted matrix to run. To install do:  
        sudo apt-get install python-twisted
   ~~~~~~~~~~
   Twisted is a framework that allows concurrent servers to be built 
   using Asynchronous connections. We'll look into these later. 


   To see how it works run the program as:  python EchoServer.py
   Then open another terminal and use telnet program to connect: 
   telnet localhost 8000

   Type whatever you want then press Enter. 
   To close the telnet connection press CTRL+] and then CTRL+D
"""

from twisted.internet import protocol, reactor
from signal import SIGINT, signal
from sys import exit
import logging as LOG
import LoggingConfig
from BlockDivider import BlockDivider, FileNotFoundException,BlockCreator,DS

from Validation import Validation, ValidationException
import os
import json

def ranGenerator():
    import random
    x=random.randint(1,100)
    return x 

class Echo(protocol.Protocol):
    connections=0
    def connectionMade(self):
              
        Echo.connections+=1               
        LOG.debug("Total connections: %d",Echo.connections)

    def dataReceived(self, data):
        print data
        LOG.info("Received data from client: %s" ,data)
        d=json.loads(data)
        print type(d)
        ID=None
        if(d[DS.CONTENT_TYPE]==DS.INIT):
            ID=ranGenerator()
        self.transport.write(BlockCreator(ID).createInit())
        
        try:
           
            v =Validation()
            LOG.info ("Current working directory %s" %(os.getcwd()))
            filename=v.validate(data)[1]
            LOG.info ("filename validated %s " %(filename))
            LOG.info ("File exists")
            bd=BlockDivider(filename,ID)
            while(bd.hasMoreData()):
                data=bd.getFileContent()
                self.transport.write(json.dumps(data))
            LOG.info ("File contents sent")
        except ValidationException:
            responseContent="Invalid query: %s" %(data)
            self.transport.write(responseContent)
        except FileNotFoundException:
            LOG.info ("File not found")
            responseContent="FileNotFound : %s" %(filename)
            self.transport.write(responseContent)

        

    def connectionLost(self,reason):
        Echo.connections-=1
        LOG.debug ("ConnectionLost, Total connections: %d " , Echo.connections)
        
    @staticmethod
    def sigintHandler(num,trace):
        LOG.info("Quitting the program")
        LOG.info("total connections %d" %(Echo.connections))
        reactor.stop()

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()
if __name__=="__main__":
    signal(SIGINT,Echo.sigintHandler)
    reactor.listenTCP(8000, EchoFactory())
    reactor.run()
