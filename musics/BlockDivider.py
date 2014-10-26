import sys
"""

File is taken as input and it checks whether the file is present or not
Once the file is present it proceeds furthur by reading the whole file and writing it into another file.

Here,BlockDivider is the class and myFunction is the function thats being called.


"""
from exceptions import Exception
import LoggingConfig
import BlockCreater
from BlockCreater import DS
import logging as LOG
class FileNotFoundException(Exception):
    pass

class BlockDivider:
      
    def __init__(self,filename):
        try:
            
            self.fd = open(filename,'r')
        except IOError:
            LOG.error("Error file not found: [%s]" %(filename))
            raise FileNotFoundException()
            
    def hasMoreData():
        pass
    
    def hasData():
        pass
    
    def getNext(self,fd,size):
        pass
    
    def getFileContent(self):
       try:
            data=BlockDivider.getNext(fd,1024)
            bc=BlockCreater(data)
            return bc.createBlock()
       except:
            return bc.createEndOfFile()
       

if __name__ == "__main__":
    filename=raw_input("Enter filename: ")
    try:
        bd =BlockDivider(filename)
        data=bd.getFileContent()
        print bd.getFileContent()
    except FileNotFoundException:
        print ("File %s does not exist" %(filename))
