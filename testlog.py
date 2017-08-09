import logging
from packages.marksql import *
logging = logging.getLogger('StartupDay')
logging.basicConfig(filename="test.log",
                    format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.DEBUG)

logging.basicConfig(filename="test.log",level=logging.DEBUG)
logging.debug(' This is debug')
logging.info(' This is info')
logging.warning(' This is a warning')
