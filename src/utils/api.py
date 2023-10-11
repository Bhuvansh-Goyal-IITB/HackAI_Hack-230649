import currencyapicom
from dotenv import load_dotenv
import os

load_dotenv()

class ApiHandler:
    def __init__(self):
        # initalize the client
        self.client = currencyapicom.Client(os.environ["CURRENCY_API_KEY"])

    # gets the currency data
    def get_currency_data(self):
        return self.client.currencies()
    
    # gets the exchange rates
    def get_latest_exchange_rates(self, base_currency, foreign_currencies):
        return self.client.latest(base_currency=base_currency, currencies=foreign_currencies)
    
apiHandler = ApiHandler()
