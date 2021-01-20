

class PaymentProcessor():

    def __init__(self, checker):
        self.gateways = [
            CheapPaymentGateway(), 
            ExpensivePaymentGateway(), 
            PremiumPaymentGateway()
        ]
        self.checker = checker

    def get_payment_gateway(self):
        for gateway in self.gateways:
            if int(self.checker.amount) > gateway.bottom_value and \
                int(self.checker.amount) <= gateway.top_value:
                return gateway.process_payment()


class PaymentGateway():
    
    def __init__(self, amount):
        self.amount = amount
    
    def process_payment(self):
        return self.name


class CheapPaymentGateway(PaymentGateway):
    def __init__(self):
        self.name = 'CheapPaymentGateway'
        self.bottom_value = 1
        self.top_value = 20
    

class ExpensivePaymentGateway(PaymentGateway):
    def __init__(self):
        self.name = 'ExpensivePaymentGateway'
        self.bottom_value = 21
        self.top_value = 500


class PremiumPaymentGateway(PaymentGateway):
    def __init__(self):
        self.name = 'PremiumPaymentGateway'
        self.bottom_value = 501
        self.top_value = 10000