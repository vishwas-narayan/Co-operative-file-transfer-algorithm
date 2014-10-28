import sys
"""

File is taken as input and it checks whether the file is present or not
Once the file is present it proceeds furthur by reading the whole file and writing it into another file.

Here,BlockDivider is the class and myFunction is the function thats being called.


"""
from exceptions import Exception
import LoggingConfig
import BlockCreater

import logging as LOG
class FileNotFoundException(Exception):
    pass

class BlockDivider:
    length=0
    def __init__(self,filename):
        
        try:
            self.fd = open(filename,'r')
            self.length=len(filename)
                
        except IOError:
            LOG.error("Error file not found: [%s]" %(filename))
            raise FileNotFoundException()
            
   
    
    def hasMoreData(self):
       storage=self.fd.read()
       if(storage==""):
           return False
       else:
           return True
    
 #   def getNext(self,fp,size):
  #      self.fd=fp
   #     return self.fd.read(size)
    
    def getFileContent(self):
       
       if(self.length>1024):
            self.length=self.length-1024
          
            data=self.fd.read(1024)
            be=BlockCreater(data)
            return be.createBlock()
       else:
            data=self.fd.read(1024)
            be=BlockCreater(data)
            return be.createEndOfFile()
       

if __name__ == "__main__":
    filename=raw_input("Enter filename: ")
    try:
        bd =BlockDivider(filename)
        data=bd.getFileContent()
        print data
    except FileNotFoundException:
        print ("File %s does not exist" %(filename))
