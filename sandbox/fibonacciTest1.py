#this code is for only reading the input from the console
def readInputFromTheConsole(numberOfElementsOfFibonacciSeries):
  listName=[0]*numberOfElementsOfFibonacciSeries
  #list initialization
  i=0
  print "enter the element's positions"
  while i<numberOfElementsOfFibonacciSeries:
    listName[i]=input()
    i=i+1
  return listName
def getListOfNumbersFromConsole():
  print "Enter the number of fibonacci elements to print"
  storeList=readInputFromTheConsole(input())
  print storeList
  return storeList
originalList=getListOfNumbersFromConsole()
