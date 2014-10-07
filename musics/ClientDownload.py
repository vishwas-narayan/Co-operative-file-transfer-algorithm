import json
import tempfile
from twisted.internet import reactor, protocol
class EchoClient(protocol.Protocol):
    def connectionMade(self):
        print "enter filename"
        variable=raw_input()
        self.transport.write(str(variable))
    def dataReceived(self,data):
        f=open("newfile.txt",'w')
        
#        f = tempfile.NamedTemporaryFile(mode='w+')
#       f.write(data)
#        d=json.loads(f)
        print "Data received: %s" %(str(data))
        try:
            d=json.loads(data)
                     
        except:
            print "Error in converting from json"
        open("filee.txt","w").write(d[u'CONTENT'])
        print "contents inside the file" %(d[u'CONTENT']) 
        f.write(d["u'CONTENT'"])   
        f.close()
#        f.write(data)
        self.transport.loseConnection()
class EchoFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed."
        reactor.stop()
    def clientConnectionLost(self, connector, reason):
        print "Connection lost."
        reactor.stop()
reactor.connectTCP("localhost",8000,EchoFactory())
reactor.run()   
