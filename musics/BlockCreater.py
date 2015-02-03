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
    CHECK="CHECK"  
    NOCHECK="NOCHECK"    
    REINIT="REINIT"
import json
class BlockCreator():
    blockNum={}
    def __init__(self,myid=None):
        self.myid=myid 
        
    def createReinit(self):
        """2.This module is used to create 'REINIT' datastructure"""   
        d={}
        d[DS.CONTENT_TYPE]=DS.REINIT
        d[DS.ID]=self.myid
        return json.dumps(d) 
             
    def createBlock(self,data):
        d={}
        d[DS.ID]=self.myid
        d[DS.BLOCKSIZE]=len(data)
        d[DS.CONTENT]=data
        d[DS.CONTENT_TYPE]=DS.DATA
        d[DS.ACK]=DS.ACK
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
        d[DS.CONTENT_TYPE]=DS.OPERATION
        d[DS.CONTENT]=data
        d[DS.ID]=self.myid
        d[DS.ACK]=DS.ACK
        d[DS.CHECK]=DS.CHECK
        return json.dumps(d)
    
    def createEndOfFile(self,data):
        d=self.createBlock(data)
        d[DS.CONTENT_TYPE]=DS.EOF
        return d
    def createInit(self):
        d={}
        d[DS.CONTENT_TYPE]=DS.INIT
        d[DS.ID]=self.myid
        return json.dumps(d)
    def createBlockForClient(self):
        LOG.debug("Inside client for acknowledgement ")
        d={}
        d[DS.CONTENT_TYPE]=DS.OPERATION
        d[DS.ACK]=DS.ACK
        d[DS.ID]=self.myid
        d[DS.CHECK]=DS.NOCHECK
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
        print ("File %s does not exist" %(filename))
      

