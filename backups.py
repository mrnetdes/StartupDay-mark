# Importing config file
with open('config.json', "r") as data_file: # Reading in JSON file to be parsed
    jsonObject = json.load(data_file) # parsing file





class Customsql(object):
    """ Mysql has the following properties:
        user:
        pw:
        host:
        port:
        database:
    """
    def __init__(self, user = "root", pw = "root", host = "localhost", port=3306, database = "lchsdb_test"):
        self.user = user
        self.pw = pw
        self.host = host
        self.port = port
        self.database = database

        self.config = {
            'user': self.user,
            'password': self.pw,
            'host': self.host,
            'port': self.port,
            'database': self.database
        }

        try:
            self.cnx = mysql.connector.connect(**self.config)
            self.cursor = self.cnx.cursor()
            #logging.info("MySQL: connection was opened on " + str(self.host))
        except mysql.connector.Error as err:
            print("Uh oh :( Please show this message to your IT Administrator")
            print(str(err))
            #logging.exception("MySQL: attempting to connect to " + str(self.host))
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                #print(str(errorcode.ER_ACCESS_DENIED_ERROR))
                logging.exception(str(errorcode.ER_ACCESS_DENIED_ERROR))
                sys.exit()
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                #print(str(errorcode.ER_ACCESS_DENIED_ERROR))
                #logging.exception(str(errorcode.ER_BAD_DB_ERROR))
                sys.exit()
            else:
                #print(err)
                #logging.exception(str(err))
                sys.exit()

    def test_connection(self):
        """
        Attempts to connect to the host, ensuring there is a connection
        """
        print ("Testing MySQL connection..."),
        try:
            cnx = mysql.connector.connect(**self.config)
            print("Connection to " + str(self.host) + " successful")
            cnx.close()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("FAIL! Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("FAIL! Database does not exist")
            else:
                print(err)

    def is_operator(self, id):
        '''
        Returns True if the given id is a valid operator - returns False otherwise
        '''
        return True

    def is_student(self, id):
        '''
        Returns True if the given id is a valid operator - returns False otherwise
        '''

        """query = "SELECT COUNT(*) FROM People WHERE IDNum=" + str(id) + " AND Status=\"Active\""
        self.cursor.execute(query)
        rows = self.cursor.fetchone()[0]
        if rows == 0:
            return False
        else:
            return True"""

    def close_connection(self):
        self.cursor.close()
        self.cnx.close()
        logging.info("MySQL: connection to " + str(self.host) + " was closed")







# Card
elif (pay_method == jsonObject['VALID_PAYMENT']['credit']['UPC']):
    comment = last_four("\tLast four digits on card: ")
    if (amount == jsonObject['VALID_PAYMENT']['pay_in_full']['UPC']):
        upcharge = float(outstanding * 0.03)
        amount = float(outstanding + upcharge)
        outstanding = 0
        print(Fore.YELLOW + "\t3% charge of $" + str(upcharge) + " being applied" + Style.RESET_ALL)
        paymentInfo.append(Payment(pay_method, amount, comment))
    else:
        """
        upcharge = float(amount * 0.03)
        print(Fore.YELLOW + "\t3% charge of $" + str(upcharge) + " being applied" + Style.RESET_ALL)
        outstanding -= amount
        outstanding += round(upcharge,2)
        paymentInfo.append(Payment(pay_method, amount, comment))
        """
        upcharge = float(amount * 0.03)
        outstanding -= amount
        #outstanding += round(upcharge,2)

        paymentInfo.append(Payment(pay_method, amount, comment))
        paymentInfo.append(Payment(str(comment) + "_fee", upcharge, comment))
