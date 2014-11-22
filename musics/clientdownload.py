import json
import tempfile
from twisted.internet import reactor, protocol
#import requests
import logging as LOG
import LoggingConfig
from BlockCreater import DS, BlockCreator
class EchoClient(protocol.Protocol):
   
    def connectionMade(self):
        self.variable=raw_input("enter filename: ")
        self.transport.write(BlockCreator().createInit())
    def dataReceived(self,data):
        LOG.debug("In client : %s" %str(type(data)))
        
        LOG.debug ("Received from server.")
        d=json.loads(data)
        if(d[DS.CONTENT_TYPE]==DS.INIT):
            self.id=d[DS.ID]
            self.transport.write(BlockCreator(self.id).forOperation(("GET " +str(self.variable))))
            
        if(d[DS.CONTENT_TYPE]==DS.DATA):
            f=open("newfile.txt",'a')     
            try: 
                f.write(d[DS.CONTENT])
                print d[DS.CONTENT]
                print 1
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
