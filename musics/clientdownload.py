import json
import tempfile
from twisted.internet import reactor, protocol
#import requests
import logging as LOG
from ipadress import ip
import LoggingConfig
from BlockCreater import DS, BlockCreator
class EchoClient(protocol.Protocol):
    def __init__(self,echoFactory,Ide=None,filename=None):
        """5.To make the created client's id same"""
        self.ef=echoFactory
        self.id=Ide
        self.variable=filename
    def connectionMade(self):
        """6.This module is for checking whether this is first connection of the client.
        If it is not then the created instance sends message to the server about its creation"""
        if(self.id==None):
            self.variable=raw_input("enter filename: ")
            self.transport.write(BlockCreator().createInit())
        else:
            LOG.debug("Created Instance makes the server check for another instance to be created")
            self.transport.write(BlockCreator(self.id).forOperation(("GET " +str(self.variable))))
        
    def dataReceived(self,data):
        LOG.debug("In client : %s" %str(type(data)))
        
        LOG.debug ("Received from server.")
        d=json.loads(data)
        if(d[DS.CONTENT_TYPE]==DS.INIT):
            self.id=d[DS.ID]
            self.transport.write(BlockCreator(self.id).forOperation(("GET " +str(self.variable))))
        if(d[DS.CONTENT_TYPE]==DS.REINIT):  
            """3.This module checks whether the server requests for creating another instance.
            And sends the message[in the form of id] to the EchoFactory which actually creates the instance"""
            LOG.debug("Reinit message recieved from server ")
            self.transport.write(BlockCreator(self.id).forOperation(("GET " +str(self.variable))))
            self.ef.getMessageFromClient(self.id,self.variable)
            
        if(d[DS.CONTENT_TYPE]==DS.DATA):
            f=open("newfile.txt",'a')     
            try: 
                f.write(d[DS.CONTENT])
                print d[DS.CONTENT]
                
                self.transport.write(BlockCreator(self.id).createBlockForClient())
                    
            except:
                LOG.debug( "Error in converting from json")
                self.transport.loseConnection()
        if(d[DS.CONTENT_TYPE]==DS.EOF):
            f=open("newfile.txt",'a')
            try:
                f.write(d[DS.CONTENT])
                f.close()
            except:
                print "Error in EOF"
            self.transport.loseConnection()   
class EchoFactory(protocol.ClientFactory):
    def __init__(self):
        self.ide=None
        self.filename=None
    def buildProtocol(self, addr):
        return EchoClient(self,self.ide,self.filename)
        
    def getMessageFromClient(self,Id,filename):
        """4.This method iniates the connection with the server but with the id.
        So that EchoFactory uses the id for creating the client"""
        LOG.debug("Message to the EchoFactory from client %d" ,Id)
        self.ide=Id
        self.filename=filename
        reactor.connectTCP("localhost",8000,self)
        LOG.debug("2nd connection is made")        

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed......"
        reactor.stop()
    def clientConnectionLost(self, connector, reason):
        print "Connection lost......"
        reactor.stop()
echoFactory=EchoFactory()
LOG.debug("1st connection is made")
reactor.connectTCP("localhost",8000,echoFactory)
reactor.run()   
