# Author: Mark Ritchie
# Part of Stephen Ritchie's StartupDay project
# Utility program to find transaction ids in the database by
# searching by last name

# Importing all the custom packages
#from packages.header import *
#from packages.validation import *
#from packages.user import *
#from packages.customsql import *
from packages.marksql import *
#from packages.payment import *
#from packages.customprint import *

import json # Support for json config file
import logging
import time
import os, sys

logdir="./logs"
logfname=os.path.join(logdir,"test.log")

logging.basicConfig(filename=logfname,mode="a",
                    format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.DEBUG)
logging.info("==== find_transaction Start")
query1 = ("select distinct itemTbl.transactionID,transactionTbl.AddDate,fname,lname "
          "from itemTbl,People,transactionTbl where lname= %s and "
          "itemTbl.IDNum=People.IDNum and itemTbl.transactionID = transactionTbl.transactionID "
          "and schoolyear=%s order by transactionTbl.AddDate")

# The marksql package will connect to the database
exitFlag = False
lname = raw_input("Enter student last name: ")
print("{0:15} {1:20} {2:15} {3:15}".format("TransactionID","Add Date","Fname","Lname"))
while (lname != ""):
  cursor.execute(query1, (lname,2017))
  
  for (transactionID, AddDate,fname, lname) in cursor:
    print("{0:15} {1:20} {2:15} {3:15}".format(transactionID, str(AddDate),fname,lname))
  lname = raw_input("Enter student last name: ")

logging.info("==== find_transaction End")
cursor.close()
cnx.close()


