import datetime
from cardvalidator import luhn


class Checker():
    
    def __init__(self, credit_card_number, card_holder, expiration_date, security_code, amount):
        self.credit_card_number = credit_card_number
        self.card_holder = card_holder
        self.expiration_date = expiration_date
        self.security_code = security_code
        self.amount = amount


    def check_data(self):
        valid_credit_card_number, message = self.check_credit_card_number()
        if not valid_credit_card_number:
            return False, {'status_code': 400, 'message': message}, 400

        valid_card_holder, message = self.check_card_holder()
        if not valid_card_holder:
            return False, {'status_code': 400, 'message': message}, 400
    
        valid_expiration_date, message = self.check_date()
        if not valid_expiration_date:
            return False, {'status_code': 400, 'message': message}, 400
    
        valid_amount, message = self.check_amount()
        if not valid_amount:
            return False, {'status_code': 400, 'message': message}, 400
        
        return True, {'status_code': 200}, 200


    def check_credit_card_number(self):
        if self.credit_card_number == '':
            return False, 'The credit card number is empty.'
        
        if not luhn.is_valid(self.credit_card_number):
            return False, 'The credit card number is not valid.'
        return True, 'Valid Credit card number.'


    def check_card_holder(self):
        if self.card_holder == '':
            return False, 'The card holder name cannot be empty.'
        return True, 'Valid card holder.'


    def check_date(self):
        if self.expiration_date == '':
            return False, 'Expiration date is empty'

        date = datetime.datetime.strptime(self.expiration_date, '%m/%y')
        if date < datetime.datetime.now():
            return False, 'Your card has already expired'
        return True, 'Valid date'
    

    def check_amount(self):
        currencies = ['$', '€']
        if self.amount == '':
            return False, 'The amount cannot be empty'
        if self.amount == '0':
            return False, 'The amount cannot be 0'
        for c in self.amount:
            if not c.isdigit():
                if c not in currencies:
                    return False, 'The currency you entered is not allowed'
        return True, 'Valid amount'
    
