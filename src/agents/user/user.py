from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from messages import *
from utils import custom_logger
import os
from dotenv import load_dotenv

load_dotenv()

CURRENCY_AGENT_ADDRESS = "{currency_agent_address}"
 
user = Agent(
    name="user",
    seed=os.environ["USER_AGENT_SEED"] or "Open Sesame"
)

fund_agent_if_low(user.wallet.address())

# Clears the storage and starts asking for base currency
@user.on_event("startup")
async def handle_start(ctx: Context):
    ctx.storage.clear()
    await ctx.send(ctx.address, BaseCurrencyInputQuery())

# Takes base currency input and verifies it 
@user.on_message(model=BaseCurrencyInputQuery, replies=CurrencyVerifyQuery)
async def handle_base_currency_verify(ctx: Context, sender: str, msg: BaseCurrencyInputQuery):
    currency = input("Enter base currency code in CAPS: ")
    await ctx.send(CURRENCY_AGENT_ADDRESS, CurrencyVerifyQuery(currency=currency))

# Takes foreign currency input and verifies it 
# if user enters -1 it starts monitoring exchange rates
@user.on_message(model=ForeignCurrencyInputQuery, replies={CurrencyVerifyQuery, StartMonitoringQuery, ForeignCurrencyInputQuery})
async def handle_foreign_currency_verify(ctx: Context, sender: str, msg: ForeignCurrencyInputQuery):
    currency = input("Enter foreign currency code in CAPS (enter -1 for completing entry): ")
    
    if currency == "-1": 
        if not ctx.storage.get("foreign-currencies"):
            custom_logger.error("No foreign currencies set")
            await ctx.send(ctx.address, ForeignCurrencyInputQuery())
            return

        try:
            period = float(input("Enter period for checking real time data (in seconds): "))
        except ValueError:
            custom_logger.error("period must be a number")
            await ctx.send(ctx.address, ForeignCurrencyInputQuery())
            return
        
        if period < 0:
            custom_logger.error("period cannot be negative")
            await ctx.send(ctx.address, ForeignCurrencyInputQuery())
            return

        print_logs = input("Do you want to print logs (y/n): ").lower() == "y"
        await ctx.send(CURRENCY_AGENT_ADDRESS, StartMonitoringQuery(print_logs=print_logs, period=period))
        return
    
    await ctx.send(CURRENCY_AGENT_ADDRESS, CurrencyVerifyQuery(currency=currency))

# handles the response for setting base currency 
# if base currency is successfully set then starts taking foreign currency
# also sets the base currency in users storage
@user.on_message(model=BaseCurrencySetResponse, replies={ForeignCurrencyInputQuery, ErrorResponse})
async def handle_base_currency_set_response(ctx: Context, sender: str, msg:BaseCurrencySetResponse):
    if msg.success:
        custom_logger.info(msg.message)
    else:
        custom_logger.error(msg.message)

    if msg.success:
        ctx.storage.set("base-currency", msg.currency)
        await ctx.send(ctx.address, ForeignCurrencyInputQuery())
    else:
        await ctx.send(ctx.address, ErrorResponse(error="base currency could not be set"))

# handles the response of adding a foreign currency 
# if foreign currency is successfully added then also adds it to user storage
@user.on_message(model=ForeignCurrencyAddResponse, replies={ForeignCurrencyInputQuery, ErrorResponse})
async def handle_foreign_currency_set_response(ctx: Context, sender: str, msg:ForeignCurrencyAddResponse):
    if msg.success:
        custom_logger.info(msg.message)
    else:
        custom_logger.error(msg.message)

    if msg.success:
        foreign_currencies = ctx.storage.get("foreign-currencies") or []
        foreign_currencies.append(msg.currency)
        ctx.storage.set("foreign-currencies", foreign_currencies)

        await ctx.send(ctx.address, ForeignCurrencyInputQuery())
    else:
        await ctx.send(ctx.address, ErrorResponse(error="foreign currency could not be set"))

# handles the currency verification response
# based on the response it redirects the flow accordingly  
@user.on_message(model=CurrencyVerifyResponse, replies={BaseCurrencyInputQuery, BaseCurrencySetQuery, ForeignCurrencyInputQuery, ForeignCurrencyAddQuery})
async def handle_verify_response(ctx: Context, sender: str, msg: CurrencyVerifyResponse):
    if msg.success:
        custom_logger.info(msg.message)
    else:
        custom_logger.error(msg.message)

    if not ctx.storage.get("base-currency"):
        if not msg.success:
            await ctx.send(ctx.address, BaseCurrencyInputQuery())
        else:
            await ctx.send(CURRENCY_AGENT_ADDRESS, BaseCurrencySetQuery(currency=msg.currency))
    else:
        if msg.currency == ctx.storage.get("base-currency"):
            custom_logger.error("Cannot set foreign currency to base currency")
            await ctx.send(ctx.address, ForeignCurrencyInputQuery())
            return
        
        foreign_currencies = ctx.storage.get("foreign-currencies") or []
        if msg.currency in foreign_currencies:
            custom_logger.error("This foreign currency is already set")
            await ctx.send(ctx.address, ForeignCurrencyInputQuery())
            return
        
        if not msg.success:
            await ctx.send(ctx.address, ForeignCurrencyInputQuery())
        else:
            min = float(input("Set min: ")) 

            if min < 0:
                custom_logger.error("Cannot set min to -ve")
                await ctx.send(ctx.address, ForeignCurrencyInputQuery())
                return
            
            max = float(input("Set max: "))

            if max < 0:
                custom_logger.error("Cannot set max to -ve")
                await ctx.send(ctx.address, ForeignCurrencyInputQuery())
                return
            
            if max <= min:
                custom_logger.error("Cannot set max less than or equal to min")
                await ctx.send(ctx.address, ForeignCurrencyInputQuery())
                return

            await ctx.send(CURRENCY_AGENT_ADDRESS, ForeignCurrencyAddQuery(currency=msg.currency, min=min, max=max))
            
# for any critical error it exits the program
@user.on_message(model=ErrorResponse)
async def handle_error(ctx: Context, sender: str, msg: ErrorResponse):
    custom_logger.critical(msg.error)
    exit()