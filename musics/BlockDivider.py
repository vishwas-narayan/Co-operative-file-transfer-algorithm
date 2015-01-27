import sys
"""

File is taken as input and it checks whether the file is present or not
Once the file is present it proceeds furthur by reading the whole file and writing it into another file.

Here,BlockDivider is the class and myFunction is the function thats being called.


"""
from exceptions import Exception
import LoggingConfig
from BlockCreater import BlockCreator,DS
import os
import logging as LOG
import random
class FileNotFoundException(Exception):
    pass
class Size():  
    BLOCK_MAX_SIZE=1024
    FILE_MAX_SIZE=1024
    LENGTH=0
    def getSize(self,filename): 
        st = os.stat(filename)
        if(Size.LENGTH==0):
            st = os.stat(filename)
            Size.LENGTH= st.st_size
            Size.LENGTH-=self.FILE_MAX_SIZE#for each instance creation fileLength keeps decreasing,to end the creation
        else:
            Size.LENGTH-=self.FILE_MAX_SIZE
        return st.st_size
    def decisionOnInstanceCreation(self):
        if(Size.LENGTH>self.FILE_MAX_SIZE):
            return True
        else:
            return False   
class BlockDivider:
    length=0
    listOfBlocks=[0]#yet to be implemented
    def __init__(self,filename,Id):
        self.bc=BlockCreator(Id)
        try:
            self.fd = open(filename,'r')
            self.length=Size().getSize(filename)
                
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
       
       if(self.length>Size.BLOCK_MAX_SIZE):
       
            print self.length
            self.data=self.fd.read(Size.BLOCK_MAX_SIZE)
            be=self.bc.createBlock(self.data)
       else:
       
           self.data=self.fd.read()
           print self.length
           print "End"
           be=self.bc.createEndOfFile(self.data)
       self.length=self.length-Size.BLOCK_MAX_SIZE
       return be     

if __name__ == "__main__":
    filename=raw_input("Enter filename: ")
    try:
        bd =BlockDivider(filename)
        data=bd.getFileContent()
        print data
    except FileNotFoundException:
        print ("File %s does not exist" %(filename))
