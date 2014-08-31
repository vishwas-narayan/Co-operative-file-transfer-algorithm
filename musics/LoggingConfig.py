import logging as LOG

LOG.basicConfig(
    filename='mylog.log',
    level=LOG.DEBUG,
    format='%(asctime)s %(levelname)s : %(module)s.%(funcName)s: %(message)s', 
    datefmt='%m/%d/%Y %I:%M:%S %p')
