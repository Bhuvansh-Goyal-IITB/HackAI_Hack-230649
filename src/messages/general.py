from uagents import Model

class Currency(Model):
    symbol: str
    code: str

class ForeignCurrencyAddQuery(Model):
    currency: str
    min: float
    max: float

class ErrorResponse(Model):
    error: str

class QueryResponse(Model):
    success: bool
    message: str

class ForeignCurrencyAddResponse(QueryResponse):
    currency: str

class CurrencyVerifyResponse(QueryResponse):
    success: bool
    currency: str

class BaseCurrencySetQuery(Model):
    currency: str

class StartMonitoringQuery(Model):
    period: float
    print_logs: bool
    
class BaseCurrencySetResponse(QueryResponse):
    currency: str

class CurrencyVerifyQuery(Model):
    currency_code: str

