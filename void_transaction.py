# Author: Mark Ritchie
# Part of Stephen Ritchie's StartupDay project
# Utility program to void or restore a transaction

import json # Support for json config file
import logging
import time
import os, sys

logdir="./logs"
# Establish the log directory
if  not os.path.isdir(logdir): os.makedirs(logdir)

logfname=os.path.join(logdir,"void.log")

logging.basicConfig(filename=logfname,mode="a",
                    format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.DEBUG)

# Importing all the custom packages
from packages.marksql import *

logging.info("==== void_transaction Start")

queryTran = ("SELECT AddDate, cashier, total_extended_cost, VOIDED "
                 "FROM transactionTbl WHERE transactionID = %s")

restoreTran = ("UPDATE transactionTbl SET VOIDED=0 "
               "WHERE transactionID = %s")

voidTran = ("UPDATE transactionTbl SET VOIDED=1 "
               "WHERE transactionID = %s")


# The marksql package will connect to the database and create cursor

transID = raw_input("Enter transaction name to be voided or restored: ")
cursor.execute(queryTran, (str(transID),))
if (cursor.rowcount == 0):
  print("\nTransaction name not found, exiting")
  cursor.close
  cnx.close
  logging.info("==== void_transaction End")
  sys.exit(0)

# save the base transaction information
row = cursor.fetchone()
rcptDate = row[0]
rcptCashier = row[1]
rcptTotal = row[2]
rcptVoid = row[3]

print("{0:15} {1:20} {2:3} $ {3:7.2f}".format(transID,str(rcptDate),rcptCashier,rcptTotal))
if (int(rcptVoid) == 1):
    print("This transaction is already voided.")
    rsp = raw_input("Do you want to restore it? (y or n)")
    if (rsp == 'y'):
        cursor.execute(restoreTran, (str(transID),))
        logging.info("Trxn "+str(transID)+ " RESTORED")
        cnx.commit()
        print("Transaction restored")
else:
    rsp = raw_input("Do you want to void this transaction? (y or n) ")
    if (rsp == 'y'):
        cursor.execute(voidTran, (str(transID),))
        logging.info("Trxn "+str(transID)+ " VOIDED")
        cnx.commit()
        print("Transaction VOIDED ")


# get the transaction details and display them


logging.info("==== void_transaction End")
cursor.close()
cnx.close()


