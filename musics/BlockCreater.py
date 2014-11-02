class FileNotFoundException(Exception):
    pass
class DS:
    BLOCK="BLOCK"
    BLOCKSIZE="BLOCKSIZE"
    CONTENT="CONTENT"
    CONTENT_TYPE="CONTENT_TYPE"
    DATA=0
    ID=1/
    EOF=5
d={}
class BlockCreater():
    def __init__(self):
        self.blockNum=1
        
       
        
    def createBlock(self,data):
        d={}
        d[DS.BLOCK]=self.blockNum
        d[DS.BLOCKSIZE]=len(data)
        d[DS.CONTENT]=data
        d[DS.CONTENT_TYPE]=DS.DATA  
        self.blockNum+=1  
        return d
    
    def createEndOfFile(self,data):
        d=self.createBlock(data)
        d[DS.CONTENT_TYPE]=DS.EOF
        return d

if __name__ == "__main__":
    filename=raw_input("ENTER FILE NAME: ")
    fp=open(filename,'r')
    try:
           bc=BlockCreater()
           data=fp.read()
           d=bc.createBlock()
           print d        
    except FileNotFoundException:
        print ("File %s does not exist" %(filename))
      

