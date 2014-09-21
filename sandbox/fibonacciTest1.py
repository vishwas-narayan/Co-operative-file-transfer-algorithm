
def getListOfNumbersFromConsole():
    print "Enter",n,"numbers"
    for i in range(n):
        numberList[i] = input()
    return numberList
    
def computeFibonacciForNumberList(numberList):
    previous = {0:0,1:1}
    fibo = {}
    def fibonacci(n):
        if previous.has_key(n):
            return previous[n]
        else:
            newValue = fibonacci(n-1) + fibonacci(n-2)
            previous[n] = newValue
            return newValue
    for i in range(n):
        fibo[numberList[i]] = fibonacci(numberList[i])
    return fibo

if __name__=="__main__":
    n = input("enter n:")
    numberList = [0]*n
    print computeFibonacciForNumberList(getListOfNumbersFromConsole())
    
    
        
