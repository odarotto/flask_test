- To install dependencies run the following on your virtual env:

    pip install -r requirements.txt -v

- To run the API execute:

    flask run --port 8080

- Example URL:

    http://localhost:8080/ProcessPayment?credit_card_number=4111111111111111&card_holder=John Smith&expiration_date=10/24&security_code=123&amount=233