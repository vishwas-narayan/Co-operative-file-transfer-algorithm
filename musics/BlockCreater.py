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

import json
class BlockCreator():
    
    def __init__(self,myid=None):
        self.blockNum=1
        self.myid=myid    
        
    def createBlock(self,data):
        d={}
        d[DS.ID]=self.myid
        d[DS.BLOCK]=self.blockNum
        d[DS.BLOCKSIZE]=len(data)
        d[DS.CONTENT]=data
        d[DS.CONTENT_TYPE]=DS.DATA
        d[DS.ACK]=DS.ACK
        self.blockNum+=1  
        return d
    
    def forOperation(self,data):
        d={}
        d[DS.CONTENT_TYPE]=DS.OPERATION
        d[DS.CONTENT]=data
        d[DS.ID]=self.myid
        d[DS.ACK]=DS.ACK
        d[DS.CHECK]=DS.CHECK
        print self.myid
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
        LOG.info("Inside client ")
        d={}
        d[DS.CONTENT_TYPE]=DS.OPERATION
        d[DS.ACK]=DS.ACK
        d[DS.ID]=self.myid
        d[DS.CHECK]=DS.NOCHECK
        print d
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
      

