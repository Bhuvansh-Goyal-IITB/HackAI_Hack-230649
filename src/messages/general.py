from uagents import Model

# Queries
class BaseCurrencyInputQuery(Model):
    pass

class ForeignCurrencyInputQuery(Model):
    pass

class ForeignCurrencyAddQuery(Model):
    currency: str
    min: float
    max: float

class BaseCurrencySetQuery(Model):
    currency: str

class StartMonitoringQuery(Model):
    period: float
    print_logs: bool

class CurrencyVerifyQuery(Model):
    currency: str

# Responses
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
    
class BaseCurrencySetResponse(QueryResponse):
    currency: str

