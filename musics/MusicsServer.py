
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
from BlockDivider import BlockDivider, FileNotFoundException,BlockCreator,DS,Size,NullError
from Validation import Validation, ValidationException
import os
import json
import time

def ranGenerator():
    import random
    x=random.randint(1,100)
    return x 

class Echo(protocol.Protocol):
    
    connections=0
    NOC={}
    
    def __init__(self,echoObject,sid):
        self.sid=sid
        self.echoObject=echoObject
        self.filename=None
        self.size=Size()
        LOG.debug("Server id created")

    def connectionMade(self):
        Echo.connections+=1               
        LOG.debug("Total connections: %d",Echo.connections)

    def dataReceived(self, data):
        self.d={}
        LOG.info("Received data from client: %s" ,data)
        self.d=json.loads(data)
        LOG.debug(type(self.d))
        try:
            if(self.d[DS.CONTENT_TYPE]==DS.OPERATION):
            
                if(self.d[DS.OPERATION]==DS.INIT):
                    self.id=ranGenerator()          
                    while(Echo.NOC.has_key(self.id)):
                        self.id=ranGenerator() 
                    Echo.NOC[self.id]=1
                    self.transport.write(BlockCreator(self.id).createInit())
            
                if(self.d[DS.OPERATION]==DS.GET):
                
                
                    v=Validation()    
                    LOG.info ("Current working directory %s" %(os.getcwd()))
                    self.filename=v.validate(self.d[DS.CONTENT])[1]
                    LOG.info ("filename validated %s " %(self.filename))
                    self.bd=BlockDivider(self.filename,self.d[DS.ID])
                    LOG.info ("File exists")
                    """1.this module is to check for the filesize. 
                    if the filesize is greater than 1024bytes,then send reInit to client.
                    increase the instance count in NOC dict"""
                
                
           
            if((self.d[DS.CONTENT_TYPE]==DS.ACK and self.d[DS.OPERATION]==DS.GET) or self.d[DS.OPERATION]==DS.GET):
                if((self.size.checkSize(self.filename)>Size.FILE_MAX_SIZE) and self.size.decisionOnInstanceCreation(Echo.NOC,self.d[DS.ID])): 
                    Echo.NOC[self.id]+=1
                    LOG.debug("Filesize is checked and instance is created")
                    self.BlockIdentifier=self.echoObject.Sync(self.d[DS.ID])
                    data=self.bd.getFileContent(self.BlockIdentifier) 
                    LOG.debug("Server %d sending data : %s" ,self.sid,(str(data)))                               
                    self.transport.write(BlockCreator(self.id).createReinit(data))
            
                else:
                    self.sendBlock(self.filename) 
        
            elif(self.d[DS.CONTENT_TYPE]==DS.ACK and self.d[DS.OPERATION]==DS.REINIT):
                self.filename=self.d[DS.CONTENT]
                self.sendBlock(self.d[DS.CONTENT])
        except ValidationException:
            responseContent="Invalid query: %s" %(data)
            self.transport.write(json.dumps(responseContent))
                
        except FileNotFoundException:
            LOG.info ("File not found")
            responseContent="FileNotFound : %s" %(self.filename)
            self.transport.write(json.dumps(responseContent));                                  
    
    def sendBlock(self,filename):
        
        try:
        
            d={}
            self.BlockIdentifier=self.echoObject.Sync(self.d[DS.ID])
            self.bd=BlockDivider(self.filename,self.d[DS.ID])
            if(self.bd.hasMoreData()):
                data=self.bd.getFileContent(self.BlockIdentifier)
                LOG.debug("Server %d sending data : %s" ,self.sid,(str(data)))                               
                self.transport.write(json.dumps(data))
                LOG.info ("File contents sent")
        except NullError:
            LOG.debug("file EOF reached")
            responseContent="File last block sent: %s" %(self.filename)
            self.transport.write(json.dumps(responseContent))                    
    
    
            

    def connectionLost(self,reason):
        Echo.connections-=1  
        LOG.debug ("ConnectionLost, Total connections: %d " , Echo.connections)
        
    @staticmethod
    def sigintHandler(num,trace):
        LOG.info("Quitting the program")
        LOG.info("total connections %d" %(Echo.connections))
        reactor.stop()

class EchoFactory(protocol.Factory):
    sid=0
    f={}
    d={}
    def buildProtocol(self, addr):
        self.sid+=1
        return Echo(self,self.sid)
    def Sync(self,ide):
            if(self.f=={}):
                self.f[ide]=Size.BLOCK_MAX_SIZE            
            elif(self.f.has_key(ide)):
                self.f[ide]=self.f[ide]+Size.BLOCK_MAX_SIZE
            else:
                self.f[ide]=Size.BLOCK_MAX_SIZE
            LOG.debug("sync %s",str(self.f))
            return self.f[ide]
            
        
echoFactory=EchoFactory()
if __name__=="__main__":
    signal(SIGINT,Echo.sigintHandler)
    reactor.listenTCP(8000, echoFactory)
    reactor.run()
