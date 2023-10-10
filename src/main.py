from uagents import Bureau
from agents import currency
from agents import user
from utils import custom_logger

if __name__ == "__main__":
    bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
    bureau.add(currency)
    custom_logger.info(f"Address of currency agent is {currency.address}")
    bureau.add(user)
    bureau.run()
