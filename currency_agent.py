from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from protocols import query_proto
from api import apiHandler

currency_agent = Agent(
    name="currency agent",
    seed="123456"
)

fund_agent_if_low(currency_agent.wallet.address())

currency_agent.include(query_proto)

@currency_agent.on_event("startup")
async def fetch_currency_data(ctx: Context):
    ctx.storage.clear()

    result = apiHandler.get_currency_data()
    ctx.storage.set("currency-data", result)
    ctx.logger.info("Fetched latest currency data")