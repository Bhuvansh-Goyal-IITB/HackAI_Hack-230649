from uagents import Bureau
from currency_agent import currency_agent
from user import user

if __name__ == "__main__":
    bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
    bureau.add(currency_agent)
    bureau.add(user)
    bureau.run()
