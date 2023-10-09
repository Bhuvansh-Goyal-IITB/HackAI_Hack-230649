from uagents import Protocol, Context
from models import  *

query_proto = Protocol(name="Query")

@query_proto.on_message(model=CurrencyVerifyQuery, replies=CurrencyVerifyResponse)
async def handle_currency_verification(ctx: Context, sender: str, msg: CurrencyVerifyQuery):
    currency_data = ctx.storage.get("currency-data")
    if not currency_data:
        await ctx.send(sender, QueryResponse(success=False, message=f"Couldnt find currency data"))
        return
    if msg.currency_code in list(currency_data["data"].keys()):
        await ctx.send(sender, CurrencyVerifyResponse(success=True, message="Currency is valid", currency=msg.currency_code))
    else:
        await ctx.send(sender, CurrencyVerifyResponse(success=False, message="Currency is invalid", currency=msg.currency_code))
         
@query_proto.on_message(model=BaseCurrencySetQuery, replies=BaseCurrencySetResponse)
async def handle_set_base_currency(ctx: Context, sender: str, msg: BaseCurrencySetQuery):
    currency_data = ctx.storage.get("currency-data")
    if not currency_data:
        await ctx.send(sender, BaseCurrencySetResponse(success=False, message=f"Couldnt find currency data"))
        return
    
    ctx.storage.set("base-currency", currency_data["data"][msg.currency])
    await ctx.send(sender, BaseCurrencySetResponse(success=True, message=f"Base Currency set to {msg.currency}"))

@query_proto.on_message(model=ForeignCurrencyAddQuery, replies=ForeignCurrencyAddResponse)
async def handle_add_foreign_currency(ctx: Context, sender: str, msg: ForeignCurrencyAddQuery):
    currency_data = ctx.storage.get("currency-data")
    if not currency_data:
        await ctx.send(sender, ForeignCurrencyAddResponse(success=False, message=f"Couldnt find currency data"))
        return

    base_currency = Currency(**ctx.storage.get("base-currency"))
    if not base_currency:
        await ctx.send(sender, ForeignCurrencyAddResponse(success=False, message="Base currency is not set"))
        return

    if base_currency.code == msg.currency:
        await ctx.send(sender, ForeignCurrencyAddResponse(success=False, message="You cannot set foreign currency to base currency. For more information on this follow this link https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
        return
    
    current_foreign_currencies = ctx.storage.get("foreign-currencies") or []

    current_foreign_currencies.append({"currency": currency_data["data"][msg.currency], "min": msg.min, "max": msg.max})

    ctx.storage.set("foreign-currencies", current_foreign_currencies)
    await ctx.send(sender, ForeignCurrencyAddResponse(success=True, message=f"Foreign currency {msg.currency} added"))

    



    


