import argparse
import json
import tempfile
from twisted.internet import reactor, protocol
import logging as LOG
from ipadress import ip
import LoggingConfig
from BlockCreater import DS, BlockCreator

parser = argparse.ArgumentParser()
parser.add_argument("start",help = "File to be transferred")
args = parser.parse_args()

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
            self.filename = args.start
            self.transport.write(BlockCreator().createInit())
        else:
            LOG.debug("Created Instance makes the server check for another instance to be created")
            self.transport.write(BlockCreator(self.id).createBlockForClient(DS.REINIT,self.filename))
    def dataReceived(self,data):
        try:
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
                LOG.debug("After reinit message is sent")    
                self.recieveBlock(self.d)
            elif(self.d[DS.CONTENT_TYPE]==DS.EOF and self.d[DS.OPERATION]==DS.GET):
                self.recieveBlock(self.d)
        except:
            LOG.debug(" %s",str(data))
            LOG.debug("problem with the recieve block" )
            self.transport.loseConnection()
    def recieveBlock(self,data):
        LOG.debug("inside recieve block")
        flag=0
        flag_dic={}
        f=open("newfile.txt",'a')
        flag_dic=self.ef.clientSync(data)
        if(flag_dic['flag']==1):
            variable=flag_dic['block'] 
            if(variable[DS.CONTENT_TYPE]==DS.DATA):    
                try: 
                    f.write(variable[DS.CONTENT])
                    self.transport.write(BlockCreator(variable[DS.ID]).createBlockForClient(DS.GET,self.filename))        
                except:
                    LOG.debug( "Error in converting from json")
                    self.transport.loseConnection()
            elif(variable[DS.CONTENT_TYPE]==DS.EOF):         
                try:
                    f.write(variable[DS.CONTENT])
                    f.close()
                except:
                    LOG.debug("")
                LOG.debug("client loses connection because EOF is reached" )
                self.transport.loseConnection() 
        else:
           return  
class EchoFactory(protocol.ClientFactory):
    noc=1
    bNum={}
    dict_store_data={}
    def __init__(self):
        self.ide=None
        self.filename=None
    def buildProtocol(self, addr):
        return EchoClient(self,self.ide,self.filename)
        
    def getMessageFromClient(self,Id,filename):
        """4.This method intiates the connection with the server but with the id.
        So that EchoFactory uses the id for creating the client"""
        LOG.debug("Message to the EchoFactory from client %d" ,Id)
        self.ide=Id
        self.filename=filename
        self.noc+=1
        reactor.connectTCP(ip.f[2],8000,self)
        LOG.debug("connection %d is made",self.noc) 
    def clientSync(self,data):
        LOG.debug("inside client syn")
        cid=data[DS.ID]
        flag_dic={} 
        flag_dic['flag']=0 #function variable
        LOG.debug("value of cid:%d",cid)
        if(self.bNum.has_key(cid)):
            if(self.bNum[cid]==data[DS.BLOCK]):
                """Here the checking is done from second block"""  
                self.bNum[cid]+=1
                flag_dic['flag']=1
                flag_dic['block']=data
                return flag_dic               
        else:
            """Here the checking is done for first block and the id is added to the bNum"""
            LOG.debug("bNum has got the new id in the client sync")
            self.bNum[cid]=1
            if(data[DS.BLOCK]==self.bNum[cid]):
                LOG.debug("for the first block")
                self.bNum[cid]+=1
                flag_dic['flag']=1
                flag_dic['block']=data
                return flag_dic  
        if(flag_dic['flag']==0):
            """Here if the block is not sent orderly then that block will be added to dictionary(buffer)"""
            LOG.debug("blocks are randomnly received")
            self.dict_store_data[cid,data[DS.BLOCK]]=data
            if(self.dict_store_data.has_key((cid,self.bNum[cid]))):
                """if there is any required block in the dictionary that should be added to the file"""
                self.bNum[cid]+=1
                flag_dic['flag']=1
                flag_dic['block']=self.dict_store_data[cid,self.bNum[cid]-1]            
            return flag_dic

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed......"
        reactor.stop()
    def clientConnectionLost(self, connector, reason):
        print "Connection lost......"
        if reactor.running:
            reactor.stop()
echoFactory=EchoFactory()
LOG.debug("1st connection is made")
reactor.connectTCP(ip.f[1],8000,echoFactory)
reactor.run()   
        




