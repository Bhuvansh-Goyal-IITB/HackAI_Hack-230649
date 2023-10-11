from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from protocols import query_proto
from utils import apiHandler, custom_logger
from dotenv import load_dotenv
import os

load_dotenv()

currency = Agent(
    name="currency",
    seed=os.environ["CURRENCY_AGENT_SEED"] or "Open Sesame"
)

fund_agent_if_low(currency.wallet.address())

currency.include(query_proto)

# fetches latest data on startup
@currency.on_event("startup")
async def fetch_currency_data(ctx: Context):
    ctx.storage.clear()
    try:
        result = apiHandler.get_currency_data()
        ctx.storage.set("currency-data", result)
        custom_logger.info("Fetched latest currency data")
    except:
        custom_logger.critical("Couldnt connect to Currency API")
        exit()