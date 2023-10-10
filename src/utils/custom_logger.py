import logging
from colorlog import ColoredFormatter

ALERT = 25 
logging.addLevelName(ALERT, "ALERT")  

class CustomLogger(logging.Logger):
    def alert(self, message, *args, **kwargs):
        if self.isEnabledFor(ALERT):
            self._log(ALERT, message, args, **kwargs)

formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-6s%(reset)s%(blue)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
        'ALERT':    'bold_red', 
    },
    secondary_log_colors={},
    style='%'
)

custom_logger = CustomLogger("currency_logger")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

custom_logger.addHandler(console_handler)
