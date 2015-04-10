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
class NullError(Exception):
    pass
class Size():  
    BLOCK_MAX_SIZE=1024
    FILE_MAX_SIZE=1024
    LENGTH=0
    i=0
    fl=0
    def checkSize(self,filename):        
        st = os.stat(filename)
        if(self.fl==0):
            st = os.stat(filename)
            #LOG.debug("Length of file is %d, file : %s" %(st.st_size, filename));
            self.fl= st.st_size
            self.fl-=self.FILE_MAX_SIZE#for each instance creation fileLength keeps decreasing,to end the creation
        else:
            self.fl-=self.FILE_MAX_SIZE
            LOG.debug("filesize is decremented")
        return st.st_size
    def getSize(self,filename):
        st = os.stat(filename)
        return st.st_size 
   
    def decisionOnInstanceCreation(self,noc,ide):
        if(self.fl>self.FILE_MAX_SIZE and noc[ide]<2):#not working since all instances create their own object for Size.
            return True
        else:
            return False   
class BlockDivider:
    length=0
    def __init__(self,filename,Id):
        self.bc=BlockCreator(Id)
        self.filename=filename
        try:
            self.fd = open(filename,'r')
            self.length=Size().getSize(self.filename)        
        except IOError:
            LOG.error("Error file not found: [%s]" %(filename))
            raise FileNotFoundException()
    
    def hasMoreData(self): 
     
      if self.length>0:
            return True
      else:
            return False   
    
    def getFileContent(self,blockRange):
       self.fd.seek(blockRange-Size.BLOCK_MAX_SIZE,0)
       self.data=self.fd.read(Size.BLOCK_MAX_SIZE)       
       if(self.length>blockRange):           
           be=self.bc.createBlock(self.data)
       else:
           print self.length
           print "End"
           if(self.data==''):
               raise NullError
           be=self.bc.createEndOfFile(self.data)
       return be         

if __name__ == "__main__":
    filename=raw_input("Enter filename: ")
    try:
        bd =BlockDivider(filename)
        data=bd.getFileContent()
        print data
    except FileNotFoundException:
        print ("File %s does not exist" %(filename))
