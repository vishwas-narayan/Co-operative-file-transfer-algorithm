


class AbstractHost():
    """Abstract host: Kept as a skeleton for design purposes."""
    def __init__(self, hostname, port):
        """Use the hostname and port as input to socket.getaddrinfo to get all interfaces
           of the host and create Interface objects of all the available Interfaces"""
        pass
    def getAllInterfaces(self):
        """This method must return all interfaces associated with the Host
           Return : List of Interface objects
        """
        pass

class Host(AbstractHost):
    """Host must override methods of the base class"""
    pass
