from packages.colorama import Fore, Back, Style# Getting pretty colors

class User(object):
    """Users have the following properties:
    Attributes:
        userid: unique id number of a user
        fname: first name
        lname: last name
        propername: full propername, since sometimes fname is a nickname
        year: the year that the user will r
        enrollment_year:

        jsonObject:
        cart:
        total:
    """

    def __init__(self, userid, fname, lname, propername, year, enrollment_year, jsonObject):
        # Personal information
        self.userid = userid
        self.fname = fname
        self.lname = lname
        self.propername = propername
        self.year = year # year user will graduate LCHS
        self.enrollment_year = enrollment_year # the school year user started at LCHS

        # Inventory and cart information
        self.jsonObject = jsonObject # item information as json object
        self.cart = {} # user's cart to hold item/amount information
        self.credits = {} #user's cart to hold item/amount of item credits

        # Adding items to cart and credits - initializing with 0 units for each item
        for item in self.jsonObject['UPC']:
            item = str(item)
            self.cart[item] = 0
            self.credits[item] = 0

    def get_total(self):
        """ Gets the total of the items in the user's cart and their credits """
        total = 0.00 # resetting total to 0
        # Adding all items in cart
        for item in self.cart:
            total += float(self.cart[item] * self.jsonObject['UPC'][item]['price'])
        # Adding all items in credit
        for item in self.credits:
            total += float(self.credits[item] * self.jsonObject['UPC'][item]['credit_price'])
        return float(total)

    def add_item(self, UPC):
        """ Increments the quantity of the given UPC in the cart. """
        self.cart[str(UPC)] += 1

    def add_credit(self, UPC):
        """ Increments the quantity of the given UPC in the credits cart """
        self.credits[str(UPC)] += 1

    def get_quantity(self, UPC):
        """ """
        return int(self.cart[str(UPC)])

    def add_to_cafe(self, amount, UPC):
        """ """
        potential_amount = int(amount + self.cart[str(UPC)])
        if (potential_amount < 0):
            print (Fore.RED + "Amount results in negative balance. Please try again." + Style.RESET_ALL)
        else:
            self.cart[str(UPC)] += int(amount)
            print(Fore.GREEN + str(amount) + " added to account " + str(self.userid) + Style.RESET_ALL)

    def is_in_cart(self, UPC):
        """ """
        if (self.cart[str(UPC)] > 0): return True
        return False
        
    def print_info(self):
        """ """
        print(str(self.lname))
        print(str(self.propername))
        print("student number: " + str(self.userid))
        print(str(self.year))
        print("Enrolled: " + str(self.enrollment_year))
        print "-"*50
        print("{0:25} {1:20} {2:7}".format("Item", "Quantity", "Cost"))
        print "-"*50
        for x in self.cart:
            name = str(self.jsonObject['UPC'][x]['name'])
            price = str(self.cart[x] * self.jsonObject['UPC'][x]['price'])
            quantity = str(self.cart[x])
            print("{0:25} {1:20} {2:7}".format(name, quantity, price))
        for x in self.credits:
            name = str("cred: ") + str(self.jsonObject['UPC'][x]['name'])
            price = str(self.cart[x] * self.jsonObject['UPC'][x]['credit_price'])
            quantity = str(self.credits[x])
            print("{0:25} {1:20} {2:7}".format(name, quantity, price))

    def print_receipt(self):
        """ """
        print(str(self.propername))
        print("student number: " + str(self.userid))
        print(str(self.year))
        print "-"*50
        print("{0:20} {1:20} {2:10}".format("Item", "Quantity", "Cost"))
        print "-"*50
        for x in self.cart:
            if (self.cart[x] > 0):
                name = str(self.jsonObject['UPC'][x]['name'])
                price = str(self.cart[x] * self.jsonObject['UPC'][x]['price'])
                quantity = str(self.cart[x])
                print("{0:20} {1:20} {2:7.2f}".format(name, quantity,float(price)))
        for x in self.credits:
            if (self.credits[x] > 0):
                name = str("cred: ") + str(self.jsonObject['UPC'][x]['name'])
                price = str(self.credits[x] * self.jsonObject['UPC'][x]['credit_price'])
                quantity = str(self.credits[x])
                print("{0:20} {1:20} {2:7.2f}".format(name, quantity,float(price)))
        print("{0:20} {1:20} {2:7.2f}".format("SUBTOTAL"," ", float(self.get_total())))
