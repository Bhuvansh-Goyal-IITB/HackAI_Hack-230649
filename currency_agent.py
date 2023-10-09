from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from protocols import query_proto
import currencyapicom
from models import QueryResponse
from dotenv import load_dotenv
import os

load_dotenv()

client = currencyapicom.Client(os.environ["CURRENCY_API_KEY"])

currency_agent = Agent(
    name="currency agent",
    seed="123456"
)
 
fund_agent_if_low(currency_agent.wallet.address())

currency_agent.include(query_proto)

@currency_agent.on_event("startup")
async def fetch_currency_data(ctx: Context):
    # result = client.currencies()
    # ctx.storage.set("currency-data", result)
    ctx.logger.info("Fetched latest currency data")