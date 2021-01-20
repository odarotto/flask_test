from processor import PaymentProcessor
from checker import Checker
from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)

@app.route('/ProcessPayment')
def process_payment():
    try:
        credit_card_number = request.args.get('credit_card_number')
        card_holder = request.args.get('card_holder')
        expiration_date = request.args.get('expiration_date')
        security_code = request.args.get('security_code')
        amount = request.args.get('amount')

        checker = Checker(credit_card_number, card_holder, expiration_date, security_code, amount)
        payment_processor = PaymentProcessor(checker)

        valid, response_body, response_code = checker.check_data()

        if not valid:
            return response_body, response_code
        else:
            gateway = payment_processor.get_payment_gateway()
            if gateway:
                return {
                    'status_code': 200,
                    'message': 'Payment processed with {}'.format(gateway),
                }, 200
            return {
                'status_code': 500,
                'message': f'Your payment could not be processed by the payment gateway.',
            }, 500
    except Exception as e:
        return {
            'status_code': 500,
            'message': f'Error: {e}',
        }, 500

