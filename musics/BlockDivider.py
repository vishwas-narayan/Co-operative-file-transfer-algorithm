import sys
"""

File is taken as input and it checks whether the file is present or not
Once the file is present it proceeds furthur by reading the whole file and writing it into another file.

Here,BlockDivider is the class and myFunction is the function thats being called.


"""
from exceptions import Exception
import LoggingConfig
from BlockCreater import BlockCreater,DS
import os
import logging as LOG
class FileNotFoundException(Exception):
    pass

FILE_MAX_LENGTH=1024
def getSize(filename):
    st = os.stat(filename)
    return st.st_size
    
class BlockDivider:
    length=0
    def __init__(self,filename):
        self.bc=BlockCreater()
        try:
            self.fd = open(filename,'r')
            self.length=getSize(filename)
                
        except IOError:
            LOG.error("Error file not found: [%s]" %(filename))
            raise FileNotFoundException()
            print "Error"
   
    
    def hasMoreData(self):
      if self.length>0:
            print self.length
            return True
      else:
            return False   
    
    def getFileContent(self):
       
       if(self.length>FILE_MAX_LENGTH):
       
            print self.length
            self.data=self.fd.read(FILE_MAX_LENGTH)
            be=self.bc.createBlock(self.data)
       else:
       
           self.data=self.fd.read()
           print self.length
           print "End"
           be=self.bc.createEndOfFile(self.data)
       self.length=self.length-FILE_MAX_LENGTH
       return be
        
       

if __name__ == "__main__":
    filename=raw_input("Enter filename: ")
    try:
        bd =BlockDivider(filename)
        data=bd.getFileContent()
        print data
    except FileNotFoundException:
        print ("File %s does not exist" %(filename))
