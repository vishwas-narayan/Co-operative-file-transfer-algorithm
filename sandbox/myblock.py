"""

File is taken as input and it checks whether the file is present or not
Once the file is present it proceeds furthur by reading the whole file and writing it into another file.

Here,BlockDivider is the class and myFunction is the function thats being called.


"""
class BlockDivider:
  def myFunction(*fileName):
    fout = None
    with open(fileName, "r") as f:
        while True:
          bufferSize = f.read()
          if not bufferSize:
            """
          we've read the entire file, so we're done.
            """
            break
          outFile = open("outFile.txt", "w")
          fout=outFile.write(bufferSize)
          outFile.close()
	  
if __name__ == "__main__":
  inFile = raw_input('File name :')
  try:	
	  isFile = open(inFile,"r")
  except IOError:
      print "File does not exist"
  block = BlockDivider()
  block.myFunction(inFile)

  

