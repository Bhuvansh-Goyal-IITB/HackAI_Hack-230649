from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from models import *


CURRENCY_AGENT_ADDRESS = "agent1qtjptsnjm3et0728c0tmr5lapqe2nrwvsycp0zhcaj44asl0f83ykfuftyd"
 
user = Agent(
    name="user",
    seed="user secret phrase"
)
 
fund_agent_if_low(user.wallet.address())

class SetBaseCurrencyQuery(Model):
    pass

class SetForeignCurrencyQuery(Model):
    pass

@user.on_event("startup")
async def handle_start(ctx: Context):
    ctx.storage.clear()
    await ctx.send(ctx.address, SetBaseCurrencyQuery())
    
@user.on_message(model=SetBaseCurrencyQuery, replies=CurrencyVerifyQuery)
async def handle_base_currency_verify(ctx: Context, sender: str, msg: SetBaseCurrencyQuery):
    currency = input("Enter base currency: ")
    await ctx.send(CURRENCY_AGENT_ADDRESS, CurrencyVerifyQuery(currency_code=currency))

@user.on_message(model=SetForeignCurrencyQuery, replies={CurrencyVerifyQuery, StartMonitoringQuery})
async def handle_foreign_currency_verify(ctx: Context, sender: str, msg: SetForeignCurrencyQuery):
    currency = input("Enter foreign currency (enter -1 for completing entry): ")
    if currency == "-1":
        await ctx.send(CURRENCY_AGENT_ADDRESS, StartMonitoringQuery(print_logs=True, period=10))
        return
    
    await ctx.send(CURRENCY_AGENT_ADDRESS, CurrencyVerifyQuery(currency_code=currency))
   
@user.on_message(model=BaseCurrencySetResponse, replies=SetForeignCurrencyQuery)
async def handle_base_currency_set_response(ctx: Context, sender: str, msg:BaseCurrencySetResponse):
    ctx.logger.info(f"{msg.message}")
    if msg.success:
        ctx.storage.set("base-currency", msg.currency)
        await ctx.send(ctx.address, SetForeignCurrencyQuery())
    # else ?

@user.on_message(model=ForeignCurrencyAddResponse, replies=SetForeignCurrencyQuery)
async def handle_foreign_currency_set_response(ctx: Context, sender: str, msg:ForeignCurrencyAddResponse):
    ctx.logger.info(f"{msg.message}")
    foreign_currencies = ctx.storage.get("foreign-currencies") or []
    foreign_currencies.append(msg.currency)
    ctx.storage.set("foreign-currencies", foreign_currencies)
    await ctx.send(ctx.address, SetForeignCurrencyQuery())

@user.on_message(model=CurrencyVerifyResponse, replies={SetBaseCurrencyQuery, BaseCurrencySetQuery, SetForeignCurrencyQuery, ForeignCurrencyAddQuery})
async def handle_verify_response(ctx: Context, sender: str, msg: CurrencyVerifyResponse):
    ctx.logger.info(msg.message)

    if not ctx.storage.get("base-currency"):
        if not msg.success:
            await ctx.send(ctx.address, SetBaseCurrencyQuery())
        else:
            await ctx.send(CURRENCY_AGENT_ADDRESS, BaseCurrencySetQuery(currency=msg.currency))
    else:
        if not msg.success or msg.currency == ctx.storage.get("base-currency"):
            await ctx.send(ctx.address, SetForeignCurrencyQuery())
        else:
            min = int(input("Set min: ")) 
            max = int(input("Set max: "))
            await ctx.send(CURRENCY_AGENT_ADDRESS, ForeignCurrencyAddQuery(currency=msg.currency, min=min, max=max))
            
@user.on_message(model=ErrorResponse)
async def handle_error(ctx: Context, sender: str, msg: ErrorResponse):
    ctx.logger.info(f"Error: {msg.error}")
    # how to end full code ??