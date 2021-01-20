import unittest
import requests
import json
from cardvalidator import luhn

def make_request(credit_card_number, card_holder, expiration_date, security_code, amount):
    url = 'http://localhost:8080/ProcessPayment'\
        '?credit_card_number={}&card_holder={}&expiration_date={}&security_code={}&amount={}'
    url = url.format(credit_card_number, card_holder, expiration_date, security_code, amount)
    
    r = requests.get(url)
    return r


class TestProcessPayment(unittest.TestCase):

    def test_rejects_wrong_card_number(self):
        wrong_card_number = "589380411000000000000"
        card_holder = "John Smith"
        expiration_date = '10/24'
        security_code = '123'
        amount = '89'

        r = make_request(
            wrong_card_number, card_holder, expiration_date, security_code, amount
        )

        if r.status_code == 500:
            print(r)

        self.assertEqual(r.status_code, 400)
        self.assertIn('The credit card number is not valid.', r.text)


    def test_rejects_empty_card_number(self):
        wrong_card_number = ""
        card_holder = "John Smith"
        expiration_date = '10/24'
        security_code = '123'
        amount = '89'

        r = make_request(
            wrong_card_number, card_holder, expiration_date, security_code, amount
        )

        self.assertEqual(r.status_code, 400)
        self.assertIn('The credit card number is empty.', r.text)


    def test_rejects_empty_card_holder_name(self):
        credit_card_number = "4111111111111111"
        card_holder = ''
        expiration_date = '10/24'
        security_code = '123'
        amount = '89'

        r = make_request(
            credit_card_number, card_holder, expiration_date, security_code, amount
        )

        self.assertEqual(r.status_code, 400)
        self.assertIn('The card holder name cannot be empty.', r.text)



    def test_rejects_invalid_amount(self):
        credit_card_number = "4111111111111111"
        card_holder = "John Smith"
        expiration_date = '10/25'
        security_code = '123'
        amount = '0'

        r = make_request(
            credit_card_number, card_holder, expiration_date, security_code, amount
        )

        self.assertEqual(r.status_code, 400)
        self.assertIn('The amount cannot be 0', r.text)


    def test_rejects_invalid_currency(self):
        credit_card_number = "4111111111111111"
        card_holder = "John Smith"
        expiration_date = '10/25'
        security_code = '123'
        amount = '89e'

        r = make_request(
            credit_card_number, card_holder, expiration_date, security_code, amount
        )

        self.assertEqual(r.status_code, 400)
        self.assertIn('The currency you entered is not allowed', r.text)


    def test_rejects_empty_amount(self):
        credit_card_number = "4111111111111111"
        card_holder = "John Smith"
        expiration_date = '10/25'
        security_code = '123'
        amount = ''

        r = make_request(
            credit_card_number, card_holder, expiration_date, security_code, amount
        )

        self.assertEqual(r.status_code, 400)
        self.assertIn('The amount cannot be empty', r.text)

    
    def test_detects_empty_date(self):
        credit_card_number = "4111111111111111"
        card_holder = "John Smith"
        expiration_date = ''
        security_code = '123'
        amount = '0'

        r = make_request(
            credit_card_number, card_holder, expiration_date, security_code, amount
        )

        self.assertEqual(r.status_code, 400)
        self.assertIn('Expiration date is empty', r.text)


    def test_rejects_expired_date(self):
        credit_card_number = "4111111111111111"
        card_holder = "John Smith"
        expiration_date = '10/19'
        security_code = '123'
        amount = '89'

        r = make_request(
            credit_card_number, card_holder, expiration_date, security_code, amount
        )

        self.assertEqual(r.status_code, 400)
        self.assertIn('Your card has already expired', r.text)


    def test_process_with_cheap_gateway(self):
        credit_card_number = "4111111111111111"
        card_holder = "John Smith"
        expiration_date = '10/25'
        security_code = '123'
        amount = '15'

        r = make_request(
            credit_card_number, card_holder, expiration_date, security_code, amount
        )

        self.assertEqual(r.status_code, 200)
        self.assertIn('Payment processed with CheapPaymentGateway', r.text)


    def test_process_with_expensive_gateway(self):
        credit_card_number = "4111111111111111"
        card_holder = "John Smith"
        expiration_date = '10/25'
        security_code = '123'
        amount = '122'

        r = make_request(
            credit_card_number, card_holder, expiration_date, security_code, amount
        )

        if r.status_code == 200:
            self.assertIn('Payment processed with ', r.text)
        if r.status_code == 500:
            self.assertIn('Your payment could not be processed.', r.text)


    def test_process_with_premium_gateway(self):
        credit_card_number = "4111111111111111"
        card_holder = "John Smith"
        expiration_date = '10/25'
        security_code = '123'
        amount = '565'

        r = make_request(
            credit_card_number, card_holder, expiration_date, security_code, amount
        )

        if r.status_code == 200:
            self.assertIn('Payment processed with ', r.text)
        if r.status_code == 500:
            self.assertIn('Your payment could not be processed by the payment gateway', r.text)


if __name__ == '__main__':
    unittest.main()