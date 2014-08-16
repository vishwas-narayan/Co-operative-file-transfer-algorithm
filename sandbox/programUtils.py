#
def get_strings_from_console():
    """ Test output of the function
Enter input string: some
Enter input string: another
Enter input string: some more
Enter input string: here's some more
Enter input string: ['some', 'another', 'some more', "here's some more"]
    """
    iList=[]
    try:
        while True :
            inValue=raw_input("Enter input string: ")
            iList.append(inValue)
    except :
        return iList


if __name__ == "__main__":
    print get_strings_from_console()
