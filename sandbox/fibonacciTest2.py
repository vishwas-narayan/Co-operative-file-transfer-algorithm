def computeFibonacciForNumberList(numberList):
  previous={0:0,1:1}  
  def fib(n):
    if previous.has_key(n):
      return previous[n]
    else:
      nv=fib(n-1)+fib(n-2)
      previous[n]=nv
      return nv
  i=0
  while i<n:
    fibonacci[numberList[i]]=fib(numberList[i])
    i=i+1
  return fibonacci  
fibonacci={}
def getListOfNumbersFromConsole():
  print "enter",n,"no"
  i=0
  while i<n:
    numberList[i]=input()
    i=i+1
  return numberList  
n=input("Enter the value of n:")
numberList=[0]*n
print computeFibonacciForNumberList(getListOfNumbersFromConsole())

