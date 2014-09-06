

from exceptions import Exception
class ValidationException(Exception):
    pass
class Validation:
    """
        Author:Sushma
        this is the class to check whether the format given to access the file is correct or not

    """

    def validate(self,inputGivenForFile):
        newFormat=inputGivenForFile.split(' ')
        newFormat1=newFormat[0]
        if(newFormat1=="GET" ):
            newFormat3=newFormat[1]
            isnewFormat=newFormat3.split('/r/n')
            return ("GET",isnewFormat[0])
            
        else:
            raise ValidationException()
        
"""if __name__=="__main__":
    validationObject=Validation()
    
    if((validationObject.validate("GET /text/page/asd.html"))==1):
        print "GET /text/page/asd.html is correct format"

    if((validationObject.validate("GET \text/page/asd.html"))!=1):
        print "GET \\text/page/asd.html is wrong format"

    if((validationObject.validate("GET/text/page/asd.html"))!=1):
        print "GET/text/page/asd.html is wrong format"    
        
    if((validationObject.validate("GET /"))!=1):
        print "GET / is wrong format"
    text=raw_input("Enter text to validate: ")
    print ("Text : %s is valid? %d" %(text,validationObject.validate(text)))
"""
