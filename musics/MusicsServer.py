
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
from BlockDivider import BlockDivider, FileNotFoundException,BlockCreator
from Validation import Validation, ValidationException
import os
class Echo(protocol.Protocol):
    connections=0
    def connectionMade(self):
        Echo.connections+=1
        LOG.debug("Total connections: %d",Echo.connections)

    def dataReceived(self, data):
        LOG.info("Received data from client: %s" ,data)
        try:
            v =Validation()
            print ("Current working directory %s" %(os.getcwd()))
            filename=v.validate(data)[1]
            print "filename validated %s " %(filename)
            bd=BlockDivider(filename)
            print "File exists"
            self.transport.write(bd.getFileContent())
            print "File contents sent"

        except ValidationException:
            responseContent="Invalid query: %s" %(data)
        except FileNotFoundException:
            print "File not found"
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
