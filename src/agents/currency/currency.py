from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from protocols import query_proto
from utils import apiHandler
from dotenv import load_dotenv
import os

load_dotenv()

currency = Agent(
    name="currency",
    seed=os.environ["CURRENCY_AGENT_SEED"] or "Open Sesame"
)

fund_agent_if_low(currency.wallet.address())

currency.include(query_proto)

@currency.on_event("startup")
async def fetch_currency_data(ctx: Context):
    ctx.storage.clear()
    
    result = apiHandler.get_currency_data()
    ctx.storage.set("currency-data", result)
    ctx.logger.info("Fetched latest currency data")