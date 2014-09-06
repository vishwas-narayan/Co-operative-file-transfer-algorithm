import sys
"""

File is taken as input and it checks whether the file is present or not
Once the file is present it proceeds furthur by reading the whole file and writing it into another file.

Here,BlockDivider is the class and myFunction is the function thats being called.


"""
from exceptions import Exception
class FileNotFoundException(Exception):
    pass


BLOCK="BLOCK"
BLOCKSIZE="BLOCKSIZE"
CONTENT="CONTENT"
class BlockCreator():
    def __init__(self):
        self.blockNum=0
    def createBlock(self,data):
        d={}
        d[BLOCK]=self.blockNum+1
        d[BLOCKSIZE]=len(data)
        d[CONTENT]=data
        return d

class BlockDivider:

    def __init__(self,filename):
        try:
            
            self.fd = open(filename,'r')
        except IOError:
            print filename
            raise FileNotFoundException()
            
    def getFileContent(self):
        bc = BlockCreator()
        content=bc.createBlock(self.fd.readlines())
        return content

if __name__ == "__main__":
    filename=raw_input("Enter filename: ")
    try:
        bd =BlockDivider(filename)
        print bd.getFileContent()
    except FileNotFoundException:
        print ("File %s does not exist" %(filename))
