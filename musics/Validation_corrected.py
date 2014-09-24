import re
class Validation:
    """Program to check for the input format
        Programmer = Sushma"""
    def validationcheck(self,inputTaken):
        flag=0
        isnew=inputTaken.split('/',1)
        """splitting the input to check for the GET statement at beginning"""
        if(isnew[0]!='GET '):
            
            return False
        
        isnew1=isnew[1].split('/',10)
        
        n=len(isnew1)
        
        i=0
        while(i<n):
            if(i<n-1):
                if(re.match(r'\w+$',isnew1[i],flags=0)==None):
                    "this pattern checks whether all the entered inputs dont have special characters" 
                    return False
                    
            if(i==n-1):
                """here i have used two cases to check for the last text in the input which
                   would be either with exension or nor Ex:Readme or Readme.txt"""
                if(re.match(r'\w+\.\w+',isnew1[i],flags=0)!=None):
                    
                    flag=1
                elif(re.match(r'\w+$',isnew1[i],flags=0)!=None):
                    
                    flag=1
                else:
                    flag=0
                if(flag==1):
                    return True
                if(flag==0):
                    return False
            i=i+1
            
a=Validation()

if(a.validationcheck("GET /ncsdycg/vjdfbvh/ncbh.tst")==True):
    print "GET /ncsdycg/vjdfbvh/ncbh.tst is true"
if(a.validationcheck("GET /ncsdycg/vjdf%bvh/ncbh")==False):
    print "GET /ncsdycg/vjdf%bvh/ncbh is false"    
if(a.validationcheck("GET /")==False):
    print "GET / is false"
if(a.validationcheck("Gte /ncsdycg/vjdfbvh/ncbh.tst")==False):
    print "Gte /ncsdycg/vjdfbvh/ncbh is false"
if(a.validationcheck("GET \hcsdycg/vjdfbvh/ncbh")==False):
    print "GET \hcsdycg/vjdfbvh/ncbh is false"
if(a.validationcheck("GET /ncsdycg*/vjdf&bvh/ncbh")==False):
    print "Gte /ncsdycg*/vjdf&bvh/ncbh is false"
if(a.validationcheck("GET /ncsdycg/vjdfbvh/ncbh")==True):
    print "GET /ncsdycg/vjdfbvh/ncbh is true"    

        
    
