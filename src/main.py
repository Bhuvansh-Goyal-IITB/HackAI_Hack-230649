from uagents import Bureau
from agents import currency
from agents import user
from utils import custom_logger
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--address", help="only shows the currency agent address", action="store_true")
    args = parser.parse_args()
    
    if args.address:
        custom_logger.info(f"Address of currency agent is {currency.address}")
    else:
        bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
        bureau.add(currency)
        bureau.add(user)
        bureau.run()
