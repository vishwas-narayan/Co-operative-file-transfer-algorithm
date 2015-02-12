import json
import tempfile
from twisted.internet import reactor, protocol
import logging as LOG
from ipadress import ip
import LoggingConfig
from BlockCreater import DS, BlockCreator
class EchoClient(protocol.Protocol):
    def __init__(self,echoFactory,Ide=None,filename=None):
        """5.To make the created client's id same"""
        self.ef=echoFactory
        self.id=Ide
        self.filename=filename
    def connectionMade(self):
        """6.This module is for checking whether this is first connection of the client.
        If it is not then the created instance sends message to the server about its creation"""
        if(self.id==None):
            self.filename=raw_input("enter filename: ")
            self.transport.write(BlockCreator().createInit())
        else:
            LOG.debug("Created Instance makes the server check for another instance to be created")
            self.transport.write(BlockCreator(self.id).createBlockForClient(DS.REINIT,self.filename))
    def dataReceived(self,data):
        LOG.debug("In client : %s" %str(data))
        self.d=json.loads(data)
        if(self.d[DS.CONTENT_TYPE]==DS.ACK and self.d[DS.OPERATION]==DS.INIT):
            self.id=self.d[DS.ID]
            self.transport.write(BlockCreator(self.id).forOperation(("GET " +str(self.filename))))
        if(self.d[DS.CONTENT_TYPE]==DS.DATA):  
            if(self.d[DS.OPERATION]==DS.REINIT):
                """3.This module checks whether the server requests for creating another instance.
                And sends the message[in the form of id] to the EchoFactory which actually creates the instance"""
                LOG.debug("Reinit message recieved from server ")
                self.ef.getMessageFromClient(self.id,self.filename)
                self.recieveBlock()
            elif(self.d[DS.OPERATION]==DS.GET):
                self.recieveBlock()
        elif(self.d[DS.CONTENT_TYPE]==DS.EOF and self.d[DS.OPERATION]==DS.GET):
             self.recieveBlock()
   
    def recieveBlock(self):
        f=open("newfile.txt",'a')     
        if(self.d[DS.CONTENT_TYPE]==DS.DATA):
            try: 
                f.write(self.d[DS.CONTENT])
                self.transport.write(BlockCreator(self.id).createBlockForClient(DS.GET,self.filename))        
            except:
                LOG.debug( "Error in converting from json")
                self.transport.loseConnection()
        elif(self.d[DS.CONTENT_TYPE]==DS.EOF):                          
            f=open("newfile.txt",'a')#has to be the filename
            try:
                f.write(self.d[DS.CONTENT])
                f.close()
            except:
                LOG.debug("")
            LOG.debug("client loses connection because EOF is reached" )
            self.transport.loseConnection() 
           
class EchoFactory(protocol.ClientFactory):
    noc=1
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
        self.noc+=1
        reactor.connectTCP("localhost",8000,self)
        LOG.debug("connection %d is made",self.noc)    

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
        




