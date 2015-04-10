import logging as LOG
class FileNotFoundException(Exception):
    pass
    

class DS:
    BLOCK="BLOCK"
    BLOCKSIZE="BLOCKSIZE"
    CONTENT="CONTENT"
    CONTENT_TYPE="CONTENT_TYPE"
    DATA="DATA"
    OPERATION="OPERATION"
    INIT="INIT"
    ID="ID"
    EOF="EOF"
    ACK="ACK"     
    REINIT="REINIT"
    GET="GET"
import json
class BlockCreator():
    blockNum={}
    def __init__(self,myid=None):
        self.myid=myid 
        
    def createReinit(self,f):
        """2.This module is used to create 'REINIT' datastructure"""   
        d=f
        d[DS.OPERATION]=DS.REINIT
        return json.dumps(d) 
             
    def createBlock(self,data):
        d={}
        d[DS.ID]=self.myid
        d[DS.BLOCKSIZE]=len(data)
        d[DS.CONTENT]=data
        d[DS.CONTENT_TYPE]=DS.DATA
        d[DS.OPERATION]=DS.GET
        if(BlockCreator.blockNum.has_key(self.myid)):
            BlockCreator.blockNum[self.myid]+=1
            LOG.debug("block number incremented %s",str(BlockCreator.blockNum))
        else:
            BlockCreator.blockNum[self.myid]=1  
            LOG.debug("block number initialized %s",str(BlockCreator.blockNum))
        d[DS.BLOCK]=BlockCreator.blockNum[self.myid]  
        return d
    
    def forOperation(self,data):
        d={}
        d[DS.ID]=self.myid
        d[DS.CONTENT_TYPE]=DS.OPERATION
        d[DS.OPERATION]=DS.GET
        d[DS.CONTENT]=data  
        return json.dumps(d)
    
    def createEndOfFile(self,data):
        d=self.createBlock(data)
        d[DS.CONTENT_TYPE]=DS.EOF
        return d
        
    def createInit(self):
        d={}
        d[DS.ID]=self.myid
        d[DS.OPERATION]=DS.INIT
        if(self.myid==None):           
            d[DS.CONTENT_TYPE]=DS.OPERATION           
        else:
            d[DS.CONTENT_TYPE]=DS.ACK
        return json.dumps(d)
        
    def createBlockForClient(self,Operation,filename):
        d={}
        d[DS.ID]=self.myid
        d[DS.CONTENT_TYPE]=DS.ACK
        d[DS.CONTENT]=filename
        d[DS.OPERATION]=Operation
        LOG.debug("Inside client for acknowledgement ")
        return json.dumps(d)

if __name__ == "__main__":
    filename=raw_input("ENTER FILE NAME: ")
    fp=open(filename,'r')
    try:
        bc=BlockCreator()
        data=fp.read()
        d=bc.createBlock()
        print d        
    except FileNotFoundException:
        print ("File %s dones not exist" %(filename))
      

