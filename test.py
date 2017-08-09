# Author: Mark Ritchie
# Date: 08/04/2017
# Version: Test driver for create_receipt function


# Importing all the custom packages
#from packages.header import *
#from packages.validation import *
#from packages.user import *
#from packages.customsql import *
from packages.marksql import *
#from packages.payment import *

import json # Support for json config file
import time


def main():

    # Variables initialization
    jsonObject = None

    #----------------------------------------------
    # Read config file (in json format)
    #----------------------------------------------
    with open('config.json', "r") as data_file: 
       jsonObject = json.load(data_file) # parsing file


    #----------------------------------------------
    # Printing Receipt
    #----------------------------------------------
    
    transaction_number = raw_input("Enter transaction number")
    create_receipt(transaction_number, jsonObject)
    cnx.close()
# End of Main
if __name__ == '__main__':
    main()
