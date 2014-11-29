
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
    NOC={}   #No of connections
    
    def __init__(self):
        self.id=None
        self.filename=None
        
    def connectionMade(self):
        Echo.connections+=1               
        LOG.debug("Total connections: %d",Echo.connections)

    def dataReceived(self, data):
        LOG.info("Received data from client: %s" ,data)
        d=json.loads(data)
        LOG.debug( type(d))
        
        if(d[DS.CONTENT_TYPE]==DS.INIT):
            if(d[DS.ID]==None):
                self.id=ranGenerator()          
                while(Echo.NOC.has_key(self.id)):
                    self.id=ranGenerator() 
                Echo.NOC[self.id]=1
                self.transport.write(BlockCreator(self.id).createInit())
            if(Echo.NOC.has_key(d[DS.ID])):
                Echo.NOC[self.id]+=1
                self.transport.write(BlockCreator(self.id).createInit())
        if(d[DS.CONTENT_TYPE]==DS.OPERATION):
                try:
                    if(d[DS.CHECK]==DS.CHECK):
                        v=Validation()
                        LOG.info ("Current working directory %s" %(os.getcwd()))
                        self.filename=v.validate(d[DS.CONTENT])[1]
                        LOG.info ("filename validated %s " %(self.filename))
                        LOG.info ("File exists")
                        self.bd=BlockDivider(self.filename,d[DS.ID])
                    
                    if(d[DS.ACK]==DS.ACK): 
                                       
                        if(self.bd.hasMoreData()):
                            data=self.bd.getFileContent()
                            LOG.debug("Server sending data : %s" %(str(data)))
                            print data
                            self.transport.write(json.dumps(data))
                            LOG.info ("File contents sent")
                except ValidationException:
                    responseContent="Invalid query: %s" %(data)
                    self.transport.write(responseContent)
                except FileNotFoundException:
                    LOG.info ("File not found")
                    responseContent="FileNotFound : %s" %(self.filename)
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
