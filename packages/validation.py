from packages.colorama import Fore, Back, Style# Getting pretty colors
import json # Support for json config file
#from packages.customsql import * # Mysql Support
from packages.marksql import cnx, cursor, is_student

import logging


# Importing config file
with open('config.json', "r") as data_file: # Reading in JSON file to be parsed
    jsonObject = json.load(data_file) # parsing file

# not done
def clean_shutdown():
    """
    Args:

    Returns:
    """
    logging.info("shutdown command was issued")
    print(Back.RED + "shutting down..." + Style.RESET_ALL)
    cnx.rollback()
    cursor.close()
    cnx.close()  # closing mysql connection
    # logging...
    exit()

# not done
def get_payment_amount(prompt, max_amount):
    """
    Args:
        prompt (str): contains the prompt that will be displayed to the screen
	max_amount (float): the maximum allowed amount i.e current balance

    Returns:
    """
    while True:
        userInput = raw_input(prompt)

        # Checking for kill command
        if (userInput == jsonObject['KILL_COMMANDS']['kill_session']['name']):
            return

        if (userInput == jsonObject['VALID_AMOUNT']['PAY IN FULL']['UPC']):
            return str(userInput)

        # Exception handling for float
        try:
            userInput = float(userInput)
        except ValueError:
            print(Fore.RED + "\tINVALID INPUT" + Style.RESET_ALL)
            continue

        # Custom validation minimum amount...NEED TO SEE WHAT MIN AND MAX SHOULD BE
        if (userInput < 0) or (userInput > max_amount):
            print(Fore.RED + "\tAMOUNT MUST BE BETWEEN 0 AND " + str(max_amount) + Style.RESET_ALL)
            continue
        else:
            break

    return float(round(userInput,2))

# not done
def get_operator(prompt):
    """
    Args:
        prompt (str): contains the prompt that will be displayed to the screen

    Returns:
    """
    while True:
        userInput = raw_input(prompt)

        # Checking for kill command
        if (userInput == jsonObject['KILL_COMMANDS']['kill_session']['name']):
            clean_shutdown()

        # Exception handling for string
        try:
            userInput = str(userInput)
        except ValueError:
            print(Fore.RED + "Invalid Input" + Style.RESET_ALL)
            continue

        # Checking that operator is valid
	if (userInput.isalpha() == False):
	   print(Fore.RED + "ID must be alphabetic characters" + Style.RESET_ALL)
	   continue

        if (len(userInput) != 3):
            print(Fore.RED + "ID must be 3 characters" + Style.RESET_ALL)
            continue
        else:
            break

    return userInput

# not done
def get_id(prompt):
    """
    Args:
        prompt (str): contains the prompt that will be displayed to the screen

    Returns:
    """
    while True:
        userInput = raw_input(prompt)

        # Checking for kill command
        if (userInput == jsonObject['KILL_COMMANDS']['kill_session']['name']):
            clean_shutdown()

        # Exception handling for int
        try:
            userInput = int(userInput)
        except ValueError:
            print(Fore.RED + "INVALID INPUT" + Style.RESET_ALL)
            continue

        # Custom validation for proper ID number
        if (is_student(userInput)):
            break
        else:
            print(Fore.RED + "STUDENT NUMBER NOT FOUND " + Style.RESET_ALL)
            continue

    return userInput

# not done
def get_item(prompt):
    """
    Args:
        prompt (str): contains the prompt that will be displayed to the screen

    Returns:
    """
    while True:
        userInput = raw_input(prompt)

        # Checking for kill command
        if (userInput == jsonObject['KILL_COMMANDS']['kill_session']['name']):
            clean_shutdown()
        else:
            break

    return userInput

# not done
def get_payment_method(prompt):
    """
    Args:
        prompt (str): contains the prompt that will be displayed to the screen

    Returns:
    """
    while True:
        userInput = raw_input(prompt)

        # Checking for kill command
        if (userInput == jsonObject['KILL_COMMANDS']['kill_session']['name']):
            clean_shutdown()

        # Custom validation for item names
        if userInput in jsonObject['VALID_PAYMENT']:
            break
        else:
            print(Fore.RED + "\tINVALID INPUT" + Style.RESET_ALL)
            continue

    return str(userInput)


def get_yes_no(prompt):
    """
    Args:
        prompt (str): contains the prompt that will be displayed to the screen

    Returns:
    """
    while True:
        userInput = raw_input(prompt+str("[y] or n ")) # getting input from user

        # Checking for kill command
        if (userInput == jsonObject['KILL_COMMANDS']['kill_session']['name']):
            clean_shutdown()

        # Checking for null, use default
        if (userInput == ""): userInput = "y"
        # Validating input is correct
        if (userInput == "y" or userInput == "n"):
            break
        else:
            print(Fore.RED + "Invalid Input" + Style.RESET_ALL)
            continue

    return str(userInput)


# not done
def last_four(prompt):
    """
    Args:
        prompt (str): contains the prompt that will be displayed to the screen

    Returns:
    """
    while True:
        userInput = raw_input(prompt)

        # Checking for kill command
        if (userInput == jsonObject['KILL_COMMANDS']['kill_session']['name']):
            clean_shutdown()

        # Exception handling for data type
        try:
            userInput = int(userInput)
        except ValueError:
            print(Fore.RED + "\tINVALID INPUT" + Style.RESET_ALL)
            continue

        if (len(str(userInput)) == 4):
            break
        else:
            print(Fore.RED + "\tINVALID INPUT" + Style.RESET_ALL)
            continue

    return int(userInput)

# not done
def get_cafe(prompt):
    """
    Args:
        prompt (str): contains the prompt that will be displayed to the screen

    Returns:
    """
    while True:
        userInput = raw_input(prompt)

        # Checking for kill command
        if (userInput == jsonObject['KILL_COMMANDS']['kill_session']['name']):
            clean_shutdown()

        # Exception handling for data type
        try:
            userList = int(userInput)
            break
        except ValueError:
            print(Fore.RED + "\tINVALID INPUT" + Style.RESET_ALL)
            continue

    return round(float(userInput),2)
