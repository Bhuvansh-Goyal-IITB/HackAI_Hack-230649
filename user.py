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
    ctx.storage.set("base-currency-set", False)
    ctx.storage.set("foreign-currencies-set", False)
    await ctx.send(ctx.address, SetBaseCurrencyQuery())
    

@user.on_message(model=SetBaseCurrencyQuery)
async def handle_base_currency_verify(ctx: Context, sender: str, msg: SetBaseCurrencyQuery):
    currency = input("Enter base currency: ")
    await ctx.send(CURRENCY_AGENT_ADDRESS, CurrencyVerifyQuery(currency_code=currency))

@user.on_message(model=SetForeignCurrencyQuery)
async def handle_foreign_currency_verify(ctx: Context, sender: str, msg: SetForeignCurrencyQuery):
    currency = input("Enter foreign currency (enter -1 for completing entry): ")
    if currency == "-1":
        ctx.storage.set("foreign-currencies-set", True)
        return
    
    await ctx.send(CURRENCY_AGENT_ADDRESS, CurrencyVerifyQuery(currency_code=currency))
   
@user.on_interval(period=1)
async def get_exchange_rates(ctx: Context):
    setup_done = ctx.storage.get('base-currency-set') and ctx.storage.get('foreign-currencies-set')
    if setup_done:
        ctx.logger.info(f"Exchange Rates")

@user.on_message(model=BaseCurrencySetResponse)
async def handle_base_currency_set_response(ctx: Context, sender: str, msg:BaseCurrencySetResponse):
    ctx.logger.info(f"{msg.message}")
    if msg.success:
        ctx.storage.set("base-currency-set", True)
        await ctx.send(ctx.address, SetForeignCurrencyQuery())

@user.on_message(model=ForeignCurrencyAddResponse)
async def handle_foreign_currency_set_response(ctx: Context, sender: str, msg:ForeignCurrencyAddResponse):
    ctx.logger.info(f"{msg.message}")
    if msg.success:
        await ctx.send(ctx.address, SetForeignCurrencyQuery())
    else:
        ctx.send(ctx.address, SetForeignCurrencyQuery())

@user.on_message(model=CurrencyVerifyResponse)
async def handle_verify_response(ctx: Context, sender: str, msg: CurrencyVerifyResponse):
    ctx.logger.info(msg.message)

    if not ctx.storage.get("base-currency-set"):
        if not msg.success:
            await ctx.send(ctx.address, SetBaseCurrencyQuery())
        else:
            await ctx.send(CURRENCY_AGENT_ADDRESS, BaseCurrencySetQuery(currency=msg.currency))

    elif not ctx.storage.get("foreign-currencies-set"):
        if not msg.success:
            await ctx.send(ctx.address, SetForeignCurrencyQuery())
        else:
            min = int(input("Set min: ")) 
            max = int(input("Set max: "))
            await ctx.send(CURRENCY_AGENT_ADDRESS, ForeignCurrencyAddQuery(currency=msg.currency, min=min, max=max))
            
@user.on_message(model=ErrorResponse)
async def handle_error(ctx: Context, sender: str, msg: ErrorResponse):
    ctx.logger.info(f"Error: {msg.error}")
    # how to end full code ??