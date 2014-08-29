class FibonacciConstructor():
    """
    FibonacciConstructor constructs and maintains a dictionary of fibonacci numbers
    """
    def __init__(self):
        self.fibsList={0:0, 1:1}
    def _nfib(self, n):
        if n not in self.fibsList:
            self.fibsList[n] = self._nfib(n-1)+self._nfib(n-2)
        return self.fibsList[n]

    def getFibonacciNumbers(self, listOfNumbers):
        """
        Takes one list of integers as input, and returns a dictionary of fibonacci numbers
        mapped as n:Fibonacci(n)
        """
        d={}
        for n in listOfNumbers:
            d[n] = self._nfib(n)
        return d

if __name__=="__main__":
    n,nList=input("Enter N: "),[]
    for i in range(n):
        nList.append(input('Enter Number'))
    print FibonacciConstructor().getFibonacciNumbers(nList)
