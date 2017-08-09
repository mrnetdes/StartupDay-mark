# Author: Stephen Ritchie
# Date: 06/07/2017
# Version: Pre-Alpha 1.0


import json # Support for json config file
import logging
import time
import os, sys
#if (os.name != "posix"): import win32print


logging.basicConfig(filename='run.log',format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)
logging.info("-----Program Started-----")

printer_name = None
DEBUGGING = False

# Importing all the custom packages
from packages.header import *
from packages.validation import *
from packages.user import *
#from packages.customsql import *
from packages.marksql import *
from packages.payment import *
from packages.customprint import *


# Getting the pretty colors set up
from packages.colorama import init
init()
from packages.colorama import Fore, Back, Style



def show_total(userList):
    """ """
    SUBTOTAL = 0
    for person in userList:
        print("")
        userList[person].print_receipt()
        SUBTOTAL += userList[person].get_total()
    print("\nSUBTOTAL = " + str(SUBTOTAL))

def dev_print(userList, paymentInfo, transaction_number):
    """ """
    print(Fore.CYAN)
    print("----DEV PRINT----")
    print("Transaction: " + str(transaction_number))
    print("")
    print("-"*55)
    print("{0:25} {1:20} {2:7}".format("Payment", "Amount", "Comment"))
    print("-"*55)
    for x in paymentInfo:
        x.printInfo()
    for x in userList:
        print("")
        userList[x].print_info()
    print(Style.RESET_ALL)


def main():

    # Variables initialization
    jsonObject = None
    lchs_test = None
    exitFlag = None
    operator_id = None
    transaction_number = None
    user_id = None
    entry = None
    userList = None
    current_user = None


    #----------------------------------------------
    # Importing item list
    #----------------------------------------------
    try:
        with open('config.json', "r") as data_file: # Reading in JSON file to be parsed
            jsonObject = json.load(data_file) # parsing file
    except IOError:
        print(Fore.RED + "Something went horribly wrong. Please show this message to you System Administrator" + Style.RESET_ALL)
        clean_shutown()

    if (DEBUGGING):
        print json.dumps(jsonObject, indent=4, sort_keys=True)
        print(Fore.YELLOW + "WARNING: program is running in debug mode" + Style.RESET_ALL)
        logging.debug('program is running in debugging mode')
    else:
        logging.info('program is running in production mode')


    exitFlag = False # boolean to control exiting of main program loop

    title() # Displaying program title

    #----------------------------------------------
    # Getting a valid operator id - THIS CAN BE ANY 4 characters
    #----------------------------------------------
    operator_id = get_operator("Enter operator initals: ")
    print(Fore.GREEN + "Hello " + str(operator_id) + "!\n" + Style.RESET_ALL)
    logging.info("operator " + str(operator_id) + " signed in")


    #------------------------------------------------------------------
    # Main program loop
    #------------------------------------------------------------------
    """ """
    while (exitFlag == False):

        #----------------------------------------------
        # Variable initialization
        #----------------------------------------------
        """ This isn't required in python, but I think should always be done for proper programming """
        transaction_number = None # used to hold a unique transaction value
        user_id = None #
        entry = None #
        userList = {}

        #----------------------------------------------
        # Getting a valid user id
        #----------------------------------------------
        """ """
        user_id = get_id("Please SCAN Student Number: ")
        # Iterating through cursor and getting results of sql query
        for row in cursor:
            fname = row[0]
            lname = row[1]
            propername = row[2]
            year = row[3]
            enrolled = row[4]

        #----------------------------------------------
        # Creating initial user
        #----------------------------------------------
        """ """
        current_user = int(user_id) # making new user the current user
        entry = {current_user: User(current_user, fname, lname, propername, year, enrolled, jsonObject)} # creating new user
        userList.update(entry) # adding user to userList

        #----------------------------------------------
        # Generating transaction number
        #----------------------------------------------
        """ Number is based off of operator's initials and ... """
        epoch_time = str(time.time())
        epoch_time = epoch_time[:-3]
        transaction_number = epoch_time + "-" + str(operator_id)
        transaction(transaction_number)

        print(Fore.MAGENTA + "current user: " + str(userList[current_user].userid) + Style.RESET_ALL)


        #------------------------------------------------------------------
        # Main scanning loop
        #------------------------------------------------------------------
        """ This loop allows the operator to scan items, or scan an id number and create a new user. """
        while True:
            userInput = get_item("\nPlease SCAN an item or student number: ")

            # Checking for break command
            if (userInput == jsonObject['KILL_COMMANDS']['ready_for_payment']['name']):break

            # Checking for cancel transaction command
            # Note, we also need to check for cancel_trans in the outer loop
            if (userInput == jsonObject['KILL_COMMANDS']['cancel_trans']['name']): break

            if (userInput == jsonObject['KILL_COMMANDS']['view_totals']['name']):
               SUBTOTAL = 0
               for person in userList:
                 userList[person].print_receipt()
                 SUBTOTAL += userList[person].get_total()
                 print("\nTOTAL = " + str(SUBTOTAL))
               continue


            #----------------------------------------------
            # Checking if input was integer (i.e student)
            #----------------------------------------------
            try:
                userInput = int(userInput)
                # Seeing if user exists
                if (is_student(userInput)):
                    # Checking if the user already exists in the transaction
                    if userList.has_key(int(userInput)):
                        print(Fore.MAGENTA + "user already exists" + Style.RESET_ALL)
                        current_user = int(userInput)
                        print(Fore.MAGENTA + "current user changed to:" + str(userList[current_user].userid) + Style.RESET_ALL)
                    # Adding new user since they don't already exist
                    else:
                        current_user = int(userInput) # making new user the current user
                        for row in cursor:
                            fname = row[0]
                            lname = row[1]
                            propername = row[2]
                            year = row[3]
                            enrolled = row[4]
                        entry = {current_user: User(current_user, fname, lname, propername, year, enrolled, jsonObject)} # creating new user
                        userList.update(entry) # adding user to userList
                        print(Fore.MAGENTA + "current user changed to:" + str(userList[current_user].userid) + Style.RESET_ALL)
                # User does not exist
                else:
                    print(Fore.RED + "User does not exist" + Style.RESET_ALL)

            #----------------------------------------------
            # Input was not an integer
            #----------------------------------------------
            except:
                #----------------------------------------------
                # Checking if input is an item in inventory
                #----------------------------------------------
                if (userInput in jsonObject['UPC']):

                    # Checking if limit has been reached
                    if (userList[current_user].get_quantity(userInput) >= int(jsonObject['UPC'][str(userInput)]['limit'])):
                        print(Fore.YELLOW + "There is a limit of " + str(jsonObject['UPC'][str(userInput)]['limit']) + " for this item" + Style.RESET_ALL)

                    # Checking for cafeteria _ NEED TO ADD FAMILY RULE
                    elif (userInput == jsonObject["UPC"]["CAFETERIA"]["UPC"]):
                        # if ...
                        cafe_amount = get_cafe("Enter amount for cafertia account: ")
                        userList[current_user].add_to_cafe(cafe_amount, userInput) # adding dollar amount to cafeteria balance

                    # NEED PAC FAMILY RULE
                    # ...
                    elif (userInput == jsonObject["UPC"]["PAC DUES"]["UPC"]):
                        found1 = False
                        for person in userList:
                            if (userList[person].is_in_cart("PAC DUES")):
                                print("PAC_DUES already exists in this transaction")
                                if (get_yes_no("Do you want to add another PAC_DUES ") == 'n'):
                                    found1 = True
                        if not found1 :
                            userList[current_user].add_item(userInput)
                            print(Fore.GREEN+userInput+" added to "+str(userList[current_user].propername)+" cart"+Style.RESET_ALL)

                    # Senior ADs rules
                    elif (int(jsonObject['UPC'][str(userInput)]['senior_only']) == 1 and userList[current_user].year != str(jsonObject["CURRENT_GRADUATION_YEAR"])):
                        print(Fore.YELLOW + 'this item available for seniors only' + Style.RESET_ALL)

                    # Senior yearbook rule
                    elif (userInput == jsonObject["UPC"]["YEARBOOK"]["UPC"] and userList[current_user].year == str(jsonObject["CURRENT_GRADUATION_YEAR"])):
                        # Checking if user already has a yearbok
                        if (userList[current_user].get_quantity(userInput) == 0):
                            print(Fore.GREEN + "First yearbook is free for seniors!" + Style.RESET_ALL)
                            userList[current_user].add_item(userInput) # adding item to user's cart
                            userList[current_user].add_credit(userInput) # adding item to user's credit
                        # Must already have at least one yearbook
                        else:
                            userList[current_user].add_item(userInput) # adding item to user's cart
                        print(Fore.GREEN + userInput + " added to " + str(userList[current_user].propername) + " cart" + Style.RESET_ALL)


                    # Must be regular item
                    else:
                        userList[current_user].add_item(userInput) # adding item to user's cart
                        #userList[current_user].add_credit(userInput) # adding credit for item to user's cart
                        print(Fore.GREEN + userInput + " added to " + str(userList[current_user].propername) + " cart" + Style.RESET_ALL)

                # Must be invalid input
                else:
                    print(Fore.RED + "INVALID INPUT" + Style.RESET_ALL)
          # End except block

        # End if While True Main Scanning loop

        if (DEBUGGING):
            for person in userList:
                print(Fore.CYAN),
                print(person, userList[person]),
                print(Style.RESET_ALL)
        print(Fore.MAGENTA + "--------------------------------------------------------------------" + Style.RESET_ALL)

        #----------------------------------------------
        # Getting payment information
        #----------------------------------------------
        """ """
        # Check for cancel_transaction
        if (userInput == jsonObject['KILL_COMMANDS']['cancel_trans']['name']):
          print(Fore.RED+"Restarting transaction, all data discarded"+Style.RESET_ALL)
          continue
        # Calculate the total in case they did not view the totals
        SUBTOTAL = 0
        for person in userList:
          #userList[person].print_receipt()
          SUBTOTAL += userList[person].get_total()

        paymentInfo = [] # structure to hold the different payments' info
        outstanding = float(round(SUBTOTAL,2)) # the remaining balance due on the transaction
        print(Fore.YELLOW + "\nWARNING: a 3% fee will be applied to credit card purchases!" + Style.RESET_ALL) # cc surcharge warning

        while (outstanding > round(0.0,2)):
            pay_method = get_payment_method("Method of payment? ($" + str(outstanding) + " outstanding): ")

            # Checking for kill command
            if (pay_method == jsonObject['KILL_COMMANDS']['kill_session']['name']):
                clean_shutdown()

            amount = get_payment_amount("\tamount: ",outstanding) # MAR

            # Checking for kill command
            if (amount == jsonObject['KILL_COMMANDS']['kill_session']['name']):
                clean_shutdown()

            #----------------------------------------------
            # Determining payment method
            #----------------------------------------------
            # Cash
            if (pay_method == jsonObject['VALID_PAYMENT']['CASH']['UPC']):
                info = "n/a"
                payment = amount
                fee = 0
                extended_payment = amount

                if (str(amount) == jsonObject['VALID_AMOUNT']['PAY IN FULL']['UPC']):
                    amount = float(outstanding)
                    payment = outstanding
                    extended_payment = outstanding  # MAR
                    outstanding = 0
                else:
                    outstanding = float(outstanding) - float(round(amount,2))

                paymentInfo.append(Payment(pay_method, payment, fee, extended_payment, info))

            # Check
            elif (pay_method == jsonObject['VALID_PAYMENT']['CHECK']['UPC']):
                info = raw_input("\tCheck number: ")
                payment = amount
                fee = 0
                extended_payment = amount

                if (amount == jsonObject['VALID_AMOUNT']['PAY IN FULL']['UPC']):
                    amount = float(outstanding)
                    payment = outstanding
                    extended_payment = outstanding
                    outstanding = 0
                else:
                    outstanding = outstanding - float((round(amount,2)))

                paymentInfo.append(Payment(pay_method, payment, fee, extended_payment, info))

            # Card
            elif (pay_method == jsonObject['VALID_PAYMENT']['CREDIT']['UPC']):
                info = last_four("\tLast four digits on card: ")

                if (amount == jsonObject['VALID_AMOUNT']['PAY IN FULL']['UPC']):
                    upcharge = float(outstanding * 0.03)
                    print(Fore.YELLOW + "\t3% charge of $" + str(upcharge) + " being applied" + Style.RESET_ALL)
                    amount = float(outstanding)
                    payment = outstanding
                    fee = upcharge
                    extended_payment = amount + upcharge  # MAR 08/04/2017 issue 13
                    extended_payment = round(extended_payment, 2)
                    outstanding = 0
                else:
                    upcharge = float(amount * 0.03)
                    # print(Fore.YELLOW + "\t3% charge of $" + str(upcharge) + " being applied" + Style.RESET_ALL)
                    payment = amount
                    fee = upcharge
                    extended_payment = amount + upcharge
                    extended_payment = round(extended_payment, 2)
                    outstanding -= amount

                paymentInfo.append(Payment(pay_method, payment, fee, extended_payment, info))

        # End of While outstanding > 0 loop

        #----------------------------------------------
        # Making sure charges are correct
        #----------------------------------------------
        print("-"*75)
        print("{0:15} {1:15} {2:15} {3:16} {4:15}".format("PaymentType", "Payment", "Fee", "extended_payment", "info"))
        print("-"*75)
        for x in paymentInfo:
            x.printInfo()
        ready_to_finish = get_yes_no("\nDo the above payments look correct?: ")
        if (ready_to_finish == "n"):
            print(Fore.RED+"Restarting transaction, all data discarded"+Style.RESET_ALL)
            continue

        #----------------------------------------------
        # Sending info to the cloud
        # Accumulate transaction total, including payment fees
        #----------------------------------------------

        #----------------------------------------------
        # Starting a MySQL transaction
        #----------------------------------------------
        #cnx.start_transaction()

        # Payment Table
        logging.info('loading info into paymentTbl')
        add_paymentTbl = ("INSERT INTO paymentTbl "
                          "(paymentType,payment,fee,extended_payment,info,transactionID) "
                          "VALUES (%s, %s, %s, %s, %s, %s)" )
        TRANS_TOTAL = 0.0
        for x in paymentInfo:
            data_receipt = (x.paymentType, x.payment, x.fee, x.extended_payment, x.info, transaction_number)
            cursor.execute(add_paymentTbl, data_receipt)
            TRANS_TOTAL += float(x.fee)

        # Item Table - not done; need to add credits
        # Credits and TRANS_TOTAL added MAR 08/04/17
        add_itemTbl = ("INSERT INTO itemTbl "
                       "(IDNum,barcode,unitcost,units,extended_cost,transactionID) "
                       "VALUES (%s, %s, %s, %s, %s, %s)")
        logging.info('loading info into itemTbl')
        for x in userList:
            for y in userList[x].cart:
                if (userList[x].cart[y] > 0):
                    IDNum = userList[x].userid
                    barcode = jsonObject['UPC'][y]['UPC']
                    unitcost = jsonObject['UPC'][y]['price']
                    units = userList[x].cart[y]
                    extended_cost = float(units * unitcost)
                    TRANS_TOTAL += float(extended_cost)

                    data_receipt = (str(IDNum), barcode, unitcost, units, extended_cost, transaction_number)
                    cursor.execute(add_itemTbl, data_receipt)
                # Add credits to itemTbl with a negative cost
                if (userList[x].credits[y] > 0):
                    IDNum = userList[x].userid
                    barcode = jsonObject['UPC'][y]['UPC']
                    unitcost = jsonObject['UPC'][y]['credit_price']
                    units = userList[x].credits[y]
                    extended_cost = float(units * unitcost)
                    TRANS_TOTAL += float(extended_cost)

                    data_receipt = (str(IDNum), barcode, unitcost, units, extended_cost, transaction_number)
                    cursor.execute(add_itemTbl, data_receipt)
             # End of for y loop
        # End of for x loop

        # Transaction Table  MAR 08/04/17 replaced 99999 with TRANS_TOTAL for total_extended_cost
        logging.info('loading info into transactionTbl')
        add_receipt = ("INSERT INTO transactionTbl "
                     "(transactionID, VOIDED, cashier, schoolyear, total_extended_cost) "
                     "VALUES (%s, %s, %s, %s, %s)")
        data_receipt = (transaction_number, 0, operator_id, jsonObject['CURRENT_SCHOOL_YEAR'], TRANS_TOTAL)
        cursor.execute(add_receipt, data_receipt)
        #----------------------------------------------
        # Committing to MySQL
        #----------------------------------------------

        cnx.commit()
        #----------------------------------------------
        # Pulling receipt from the cloud
        #----------------------------------------------
        #dev_print(userList, paymentInfo, transaction_number)




        #----------------------------------------------
        # Committing to MySQL
        #----------------------------------------------

        cnx.commit()
        transaction_end(transaction_number)
        create_receipt(transaction_number, jsonObject)

        #----------------------------------------------
        # Printing Receipt
        #----------------------------------------------
        # ...
        print(Fore.MAGENTA + "Printing first receipt..." + Style.RESET_ALL)

        print_receipt(transaction_number,printer_name,jsonObject)
        userInput = raw_input("Press Enter to print second receipt")
        print(Fore.MAGENTA+"Printing second receipt..."+Style.RESET_ALL)
        print_receipt(transaction_number,printer_name,jsonObject)


        #clean_shutdown()
        #break

if __name__ == '__main__':
    main()
