import random

class PaymentProcessor():

    def __init__(self, checker):
        self.gateways = [
            CheapPaymentGateway(checker), 
            ExpensivePaymentGateway(checker), 
            PremiumPaymentGateway(checker)
        ]
        self.checker = checker

    def get_payment_gateway(self):
        for gateway in self.gateways:
            if int(self.checker.amount) > gateway.bottom_value and \
                int(self.checker.amount) <= gateway.top_value:
                return gateway.process_payment()


class PaymentGateway():
    
    def __init__(self):
        self.name = 'PaymentGateway'
    
    def process_payment(self):
        return self.name

    def available(self):
        availability = random.randint(55, 100)
        if availability > 75:
            return True
        return False


class CheapPaymentGateway(PaymentGateway):
    def __init__(self, checker):
        self.name = 'CheapPaymentGateway'
        self.bottom_value = 1
        self.top_value = 20
        self.checker = checker


    def process_payment(self):
        return self.name
    

class ExpensivePaymentGateway(PaymentGateway):
    def __init__(self, checker):
        self.name = 'ExpensivePaymentGateway'
        self.bottom_value = 21
        self.top_value = 500
        self.checker = checker


    def process_payment(self):
        if self.available():
            return self.name
        else:
            print('Retrying with CheapGateway')
            return CheapPaymentGateway(self.checker.amount).process_payment()


class PremiumPaymentGateway(PaymentGateway):
    def __init__(self, checker):
        self.name = 'PremiumPaymentGateway'
        self.bottom_value = 501
        self.top_value = 10000
        self.checker = checker


    def process_payment(self):
        tries = 3
        times = 1
        while True:
            if self.available():
                return self.name
            times += 1
            if times >= 3:
                return None
