from uagents import Protocol, Context
from messages import  *
import asyncio
from utils import apiHandler, custom_logger

query_proto = Protocol(name="Query")

# verifies the currency sent
@query_proto.on_message(model=CurrencyVerifyQuery, replies={CurrencyVerifyResponse, ErrorResponse})
async def handle_currency_verification(ctx: Context, sender: str, msg: CurrencyVerifyQuery):
    currency_data = ctx.storage.get("currency-data")
    
    if not currency_data:
        await ctx.send(sender, ErrorResponse(success=False, message=f"Couldnt find currency data"))
        return
    
    if msg.currency in list(currency_data["data"].keys()):
        await ctx.send(sender, CurrencyVerifyResponse(success=True, message="Currency is valid", currency=msg.currency))
    else:
        await ctx.send(sender, CurrencyVerifyResponse(success=False, message="Currency is invalid", currency=msg.currency))

# sets the base currency
@query_proto.on_message(model=BaseCurrencySetQuery, replies=BaseCurrencySetResponse)
async def handle_set_base_currency(ctx: Context, sender: str, msg: BaseCurrencySetQuery):    
    ctx.storage.set("base-currency", msg.currency)
    await ctx.send(sender, BaseCurrencySetResponse(success=True, message=f"Base Currency set to {msg.currency}", currency=msg.currency))

# starts monitoring the exchange rates 
@query_proto.on_message(model=StartMonitoringQuery, replies={ErrorResponse, StartMonitoringQuery})
async def start_monitoring(ctx: Context, sender: str, msg: StartMonitoringQuery):
    foreign_currencies = ctx.storage.get("foreign-currencies")
    base_currency = ctx.storage.get("base-currency")
    currency_data = ctx.storage.get("currency-data")

    if not currency_data:
        await ctx.send(sender, ErrorResponse(message=f"Couldnt find currency data"))
        return

    if not foreign_currencies:
        await ctx.send(sender, ErrorResponse(message=f"No foreign currencies set"))
        return
    
    if not base_currency:
        await ctx.send(sender, ErrorResponse(message=f"Base currency not set"))
        return

    exchange_data = apiHandler.get_latest_exchange_rates(base_currency=base_currency, foreign_currencies=[curr['currency'] for curr in foreign_currencies])

    for currency_object in foreign_currencies:
        currency = currency_object['currency']
        min = float(currency_object['min'])
        max = float(currency_object['max'])

        value = round(float(exchange_data['data'][currency]['value']), 2)

        if msg.print_logs:
            custom_logger.info(f"{currency_object['currency']} -> {value} {currency_data['data'][currency]['symbol']}")
        
        if min > value:
            custom_logger.alert(f"{currency_object['currency']} is lower than {min} {currency_data['data'][currency]['symbol']}")

        if max < value:
            custom_logger.alert(f"{currency_object['currency']} is higher than {max} {currency_data['data'][currency]['symbol']}")

        print("")

    await asyncio.sleep(msg.period)
    await ctx.send(ctx.address, msg)

# adds a foreign currency
@query_proto.on_message(model=ForeignCurrencyAddQuery, replies=ForeignCurrencyAddResponse)
async def handle_add_foreign_currency(ctx: Context, sender: str, msg: ForeignCurrencyAddQuery):
    foreign_currencies = ctx.storage.get("foreign-currencies") or []

    foreign_currencies.append({"currency": msg.currency, "min": msg.min, "max": msg.max})

    ctx.storage.set("foreign-currencies", foreign_currencies)
    await ctx.send(sender, ForeignCurrencyAddResponse(success=True, message=f"Foreign currency {msg.currency} added", currency=msg.currency))
