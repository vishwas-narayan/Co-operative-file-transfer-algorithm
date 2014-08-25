#to read from console

def getListOfNumbersFromConsole():
  n=input("enter n:")
  numberList=[0]*n
  print "enter",n,"numbers"
  i=0
  while i<n:
    numberList[i]=input()
    i=i+1
  print numberList

getListOfNumbersFromConsole()
  
