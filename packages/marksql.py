# MySQL functionality
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import sys
import json
import logging
import os, sys


# Importing config file
with open('mysql.json', "r") as mysql_file: # Reading in JSON file to be parsed
    jsonObjectSQL = json.load(mysql_file) # parsing file
# Setup the values for the MySQL connect
# Determining which db to connect to based on the set environment
user = jsonObjectSQL['USER']
pw = jsonObjectSQL['PW']
host = jsonObjectSQL['HOST']
port = jsonObjectSQL['PORT']
database = jsonObjectSQL['DATABASE']
config = {'user': user, 'password': pw, 'host': host, 'port': port, 'database': database}

# Attempting to open connection to specified db
logging.info("MySQL: Connecting to "+str(database)+" on "+str(host))
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    logging.info("MySQL: connected to "+str(database)+" on " + str(host))
except mysql.connector.Error as err:
    print("Uh oh :( Please show this message to your IT Administrator")
    print(str(err))
    logging.error("MySQL: " + str(err))
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        #print(str(errorcode.ER_ACCESS_DENIED_ERROR))
        #logging.exception(str(errorcode.ER_ACCESS_DENIED_ERROR))
        sys.exit()
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        #print(str(errorcode.ER_ACCESS_DENIED_ERROR))
        #logging.exception(str(errorcode.ER_BAD_DB_ERROR))
        sys.exit()
    else:
        #print(err)
        #logging.exception(str(err))
        sys.exit()

def is_student(id):
    '''
    Returns True if the given id is a valid operator - returns False otherwise. If true then info about the user is stored in the cursor.
    '''
    query = "SELECT Fname, Lname, Pname, GradClass, EnrollYear FROM People WHERE IDNum=" + str(id) + " AND Status=\"Active\""
    #query = "SELECT COUNT(*) FROM People WHERE IDNum=" + str(id) + " AND Status=\"Active\""
    cursor.execute(query)
    #rows = cursor.fetchone()[0]
    rows = cursor.rowcount
    #print(cursor.rowcount)
    if rows == 0:
        return False
    else:
        return True


# Function to create a receipt from the database
def create_receipt(transactionID, jsonObject):

   queryTran = ("SELECT AddDate, cashier, total_extended_cost "
                "FROM transactionTbl WHERE transactionID = %s "
                "AND VOIDED = 0")
   queryItem = ("SELECT itemTbl.IDNum,barcode,units,extended_cost,Lname, "
            "Pname, GradClass "
	        "FROM itemTbl,People WHERE transactionID = %s AND "
            "itemTbl.IDNum = People.IDNum "
	        "ORDER BY IDNum")
   queryPay = ("SELECT paymentType,extended_payment,info "
               "FROM paymentTbl WHERE transactionID = %s ")
   queryFee = ("SELECT fee,info FROM paymentTbl WHERE transactionID = %s AND "
              "paymentType = 'credit'")
 
   # Get receipt base directory from jsonObject
   basedir = jsonObject["RCPT_DIR"]
   f1name = os.path.join(basedir,transactionID)
   f1name = f1name+".txt"
   # Establish the receipt directory
   if  not os.path.isdir(basedir):os.makedirs(basedir)
    

   
   # Try to get the transaction info
   curA = cnx.cursor(buffered=True)
   curA.execute(queryTran, (transactionID, ))
   if (curA.rowcount == 0):
	print("\nINVALID TRANSACTION: " + str(transactionID))
	return
  
   # Now save the base transaction values
   rowA = curA.fetchone()
   rcptDate = rowA[0]
   rcptCashier = rowA[1]
   rcptTotal = rowA[2]
   
   f1 = open(f1name,"w")
   # Output header lines
   f1.write("--LCHS STARTUP DAY-- \n")
   f1.write("{0:^20}\n".format(str(rcptDate)))
   f1.write("Cashier: " + str(rcptCashier) + "\n")
   f1.write("Tran {0:15}\n\n".format(transactionID))
   # Now get all items in the transaction
   curA.execute(queryItem, (transactionID, ))
   #rowA = curA.cursor()
   #f1.write("{0:10} {1:4} {2:>6}\n".format("Item","Qty","Cost"))
   #f1.write("_"*20 + "\n")
   oldNum = None
   id_subtotal = 0.0
   tran_total = 0.0
   for (IDNum, barcode,units,extended_cost,lname,pname,gradclass) in curA:
      if (oldNum == None):  # first time, print header
         f1.write("Student: {0:11d}\n".format(IDNum))
         f1.write("{0:20.20}\n".format(lname))
         f1.write("{0:20.20}\n".format(pname))
         f1.write("{0:-<20}\n".format(gradclass))
      if ((IDNum != oldNum) and (oldNum != None)): # new IDNum
        f1.write("-"*20+"\n")
        f1.write("{0:12}${1:7.2f}\n".format("SUBTOTAL",id_subtotal))
        tran_total = tran_total + float(id_subtotal)
        id_subtotal = 0.0
        f1.write("\nStudent: {0:11d}\n".format(IDNum))
        f1.write("{0:20.20}\n".format(lname))
        f1.write("{0:20.20}\n".format(pname))
        f1.write("{0:-<20}\n".format(gradclass))
     
      name = jsonObject['UPC'][barcode]['name']
      if (barcode == "CAFETERIA"):
        f1.write("{0:8.8} {1:3} {2:7.2f}\n".format(name," ",extended_cost))
      else:
        f1.write("{0:8.8} {1:3d} {2:7.2f}\n".format(name, units, extended_cost))
      id_subtotal = id_subtotal + float(extended_cost)
      oldNum = IDNum
   # print out last IDNum subtotal
   f1.write("-"*20+"\n")
   f1.write("{0:12}${1:7.2f}\n".format("SUBTOTAL",id_subtotal))
   tran_total = tran_total + float(id_subtotal)

   # print out the transaction total, before fees
   f1.write("\n\n\n{0:12}${1:7.2f}\n".format("TOTAL",tran_total))

   # Now get any fees and add them
   curA.execute(queryFee, (transactionID, ))
   fee = 0.0
   for (fee, info) in curA:
      f1.write("{0:8}{1:5.5} {2:6.2f}\n".format("CC Fee",info,fee))

   # Now print out the grand total amount due
   f1.write("{0:12}${1:7.2f}\n".format("AMT DUE",float(rcptTotal)))
   
   # Now get the payment information
   f1.write("\nPayments\n")
   pay_total = 0.0
   curA.execute(queryPay, (transactionID, ))
   for (paymentType, extended_payment, info) in curA:
       if(paymentType == "CREDIT"): paymentType = "CARD"
       f1.write("{0:6.6} {1:5.5} {2:7.2f}\n".format(paymentType,info,float(extended_payment)))
       pay_total = pay_total + float(extended_payment)

   f1.write("-"*20+"\n")
   f1.write("{0:12}${1:7.2f}\n".format("AMT PAID",pay_total))
   f1.write("\n{0:^20}\n".format("THANK YOU"))
   f1.write("{0:^20}\n".format("Go Knights!"))
   curA.close()
   f1.close()
   return
# End create_receipt
