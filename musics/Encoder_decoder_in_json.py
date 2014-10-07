import json

class Encoder_decoder:
    """this class contains both json-encoder and json-decoder function"""
    contentSize=0
    dict_io_nary={}
    subBlockIncrementer=1
    blockIncrementer=1
    def __init__(self,counter):
        """This function is for initializing the value of block"""
        self.blockIncrementer=counter     
    def encoderFunction(self,subCounter,n):
        """This funtion takes a block of file,creates a dictionary and repeated calling of this function creates number of subBlocks for the given Block"""    
        self.subBlockIncrementer=subCounter
        self.contentSize=n
  
        self.dict_io_nary['BLOCK']=self.blockIncrementer
        self.dict_io_nary['SUBBLOCK']=self.subBlockIncrementer                
        self.dict_io_nary['CONTENT']=self.fileContent
        self.dict_io_nary['CONTENTSIZE']=self.contentSize                          
        self.encodedData=json.dumps(self.dict_io_nary,sort_keys=True)
        self.fileContent=fileP.read(self.contentSize)      
        return self.encodedData
        
    def decoderFunction(self,s):
        """This function takes the encoded dictionary and decodes it """
        self.dict_io_nary=s
        self.decodedData=json.loads(self.dict_io_nary)
        return self.decodedData    

if __name__=="__main__":
    """here the counter value(Block value) is given by the Blockdivider module.By default I had given it as '1' because here iam concentrating more on dividing this Block into subBlocks and encoding or encoding the entire Block.I had allocated 1000 memory spaces for the lists 'encodedBlock' and 'decodedBlock'by default where I would store all the Encoded and decoded data"""
    counter=1
    obj=Encoder_decoder(counter)
    encodedBlock=[0]*1000
    decodedBlock=[0]*1000
    try:
        """This 'try' statement is for the Blockdivider module to call for json-encoder for encoding the block or subBlock"""
        fileP=open("Inputfile_for_json.txt","r")
        n=input("Enter the size of the subBlock file ")
        obj.fileContent=fileP.read(n)  
        i=0
        print "-------------------------------------------------Encoded list of dictionaries-------------------------------------------"
        print "[",
        while(True):
            if(obj.fileContent==""):
                break
            else:
                encodedBlock[i]=obj.encoderFunction(i,n)
                print encodedBlock[i],",",
            i=i+1
        print "]"
    
    except IOError:
        print 'code faced problem in fetching the file'
    
    try:
        """This 'try and except' statement is for the client to call the json-decoder to decode the encodedBlock"""
        k=0
        print "--------------------------------------------------Decoded list of dictionaries-------------------------------------------"
        print "[",
        while(True):
            if(encodedBlock[k]==0):
                break
            else:
                decodedBlock[k]=obj.decoderFunction(encodedBlock[k])
                print decodedBlock[k],",",
            k=k+1       
        print "]"
    except IOError:
        print 'code faced problem in fetching the file'               
            
            
           
      

