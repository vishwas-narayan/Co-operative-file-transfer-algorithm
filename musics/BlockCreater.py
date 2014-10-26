class FileNotFoundException(Exception):
    pass
class DS:
    BLOCK="BLOCK"
    BLOCKSIZE="BLOCKSIZE"
    CONTENT="CONTENT"
    CONTENT_TYPE="CONTENT_TYPE"
    DATA=0
    ID=1
    EOF=5
d={}
class BlockCreater():
    def __init__(self,data):
        self.blockNum=0
        
        d[DS.BLOCK]=self.blockNum+1
        d[DS.BLOCKSIZE]=len(data)
        d[DS.CONTENT]=data
        d[DS.CONTENT_TYPE]=DS.DATA
        
    def createBlock(self):
        return d
    
    def createEndOfFile(self):
        d[DS.CONTENT_TYPE]=DS.EOF

if __name__ == "__main__":
    filename=raw_input("ENTER FILE NAME: ")
    fp=open(filename,'r')
    try:
           bc=BlockCreater(fp.read())
           print bc.createBlock()        
    except FileNotFoundException:
        print ("File %s does not exist" %(filename))
      

