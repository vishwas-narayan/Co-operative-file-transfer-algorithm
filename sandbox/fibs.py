def _nfib(n):
    return n if n<2 else _nfib(n-1)+_nfib(n-2)

def getFibonacciNumbers(listOfNumbers):
    d={}
    for n in listOfNumbers:
        d[n]=_nfib(n)
    return d

if __name__=="__main__":
    n,nList=input("Enter N: "),[]
    for i in range(n):
        nList.append(input('Enter Number'))
    print getFibonacciNumbers(nList)
