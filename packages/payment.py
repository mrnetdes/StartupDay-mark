class Payment(object):
    """
    Stores information about a payment.

    Args:
        type (str): contains the payment method (cash, check, card, etc)
        amount (float): contains the amount in dollars of the payment
        memo (str): field that contains additional info - For example, it will contain the last 4 digits of a cc or the check number of a check

    Attributes:
        type (str): contains the payment method (cash, check, card, etc)
        amount (float): contains the amount in dollars of the payment
        memo (str): field that contains additional info - For example, it will contain the last 4 digits of a cc or the check number of a check
    """

    def __init__(self, paymentType, payment, fee, extended_payment, info):
        self.paymentType = paymentType
        self.payment = payment
        self.fee = fee
        self.extended_payment = extended_payment
        self.info = info

    def printInfo(self):
        """ Prints out the attributes of the object """
        print("{0:15} {1:15} {2:15} {3:16} {4:15}".format(str(self.paymentType), str(self.payment), str(self.fee), str(self.extended_payment), str(self.info),))
