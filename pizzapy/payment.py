import re


class CreditCard(object):
    """A CreditCard represents a credit card.

    There's some sweet logic in here to make sure that the type of card
    you passed is valid. 
    """
    def __init__(self, number='', expiration='', cvv='', zip=''):
        self.name = ''
        print("name is", self.name)
        self.number = str(number).strip()
        print("num is", self.number)

        self.card_type = self.find_type()
        print("card_type is", self.card_type)
        self.expiration = str(expiration).strip()
        print("expiration is", self.expiration)
        self.cvv = str(cvv).strip()
        print("cvv is", self.cvv)
        self.zip = str(zip).strip()
        print("zip is", self.zip)
        if not self.validate():
            raise Exception("Invalid Card.")

    def __repr__(self):
        return "Credit Card with last four #{}".format(self.number[-4:])

    def validate(self):
        is_valid = self.number.isdigit() and len(self.number) == 16 and self.card_type != "" and len(self.expiration) == 4 and self.expiration.isdigit()
        print("valid1",is_valid)
        is_valid &= len(self.cvv) == 3 and self.cvv.isdigit()
        print("valid2",is_valid)

        is_valid &= (5 <= len(self.zip) >= 6)
        print("valid3",is_valid)

type(self):
        patterns = {'VISA': r'^4[0-9]{12}(?:[0-9]{3})?$',
                    'MASTERCARD': r'^5[1-5][0-9]{14}$',
                    'AMEX': r'^3[47][0-9]{13}$',
                    'DINERS': r'^3(?:0[0-5]|[68][0-9])[0-9]{11}$',
                    'DISCOVER': r'^6(?:011|5[0-9]{2})[0-9]{12}$',
                    'JCB': r'^(?:2131|1800|35\d{3})\d{11}$',
                    'ENROUTE': r'^(?:2014|2149)\d{11}$'}
        return next((card_type for card_type, pattern in list(patterns.items())
                     if re.match(pattern, self.number)), '')
