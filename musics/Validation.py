    
class Validation:
	"""
	Author:Sushma
	this is the class to check whether the format given to access the file is correct or not
	
    """

	def checkValidation(self,inputGivenForFile):
		newFormat=inputGivenForFile.split('/',1)
        newFormat1=newFormat[0]
    	if(newFormat1=="GET " and newFormat[1]!=''):
    		return 1
    	else:
        	return 0

validationObject=Validation()

if((validationObject.checkValidation("GET /text/page/asd.html"))==1):
	print "GET /text/page/asd.html is correct format"

if((validationObject.checkValidation("GET \text/page/asd.html"))!=1):
	print "GET \\text/page/asd.html is wrong format"

if((validationObject.checkValidation("GET/text/page/asd.html"))!=1):
	print "GET/text/page/asd.html is wrong format"    

if((validationObject.checkValidation("GET /"))!=1):
	print "GET / is wrong format"
