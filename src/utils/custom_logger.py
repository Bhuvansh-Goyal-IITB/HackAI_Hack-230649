import logging
from colorlog import ColoredFormatter

# adding custom levels
ALERT = 25 
logging.addLevelName(ALERT, "ALERT")  

QUESTION = 26
logging.addLevelName(QUESTION, "QUESTION")

class CustomLogger(logging.Logger):
    def alert(self, message, *args, **kwargs):
        if self.isEnabledFor(ALERT):
            self._log(ALERT, message, args, **kwargs)
    
    def question(self, message, *args, **kwargs):
        if self.isEnabledFor(QUESTION):
            self._log(QUESTION, message, args, **kwargs)

# color formatting
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': "\033[1;36m",        # Cyan
        'INFO': "\033[1;32m",         # Green
        'WARNING': "\033[1;33m",      # Yellow
        'ERROR': "\033[1;31m",        # Red
        'CRITICAL': "\033[1;41;97m",  # White on Red 
        'ALERT': "\033[1;35m",        # Magenta 
        'QUESTION': "\033[1;34m",     # Blue 
        'RESET': "\033[0m"            # Reset to default colors
    }
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        message = super().format(record)
        return f"{log_color}{record.levelname} - {message}{self.COLORS['RESET']}"

# setting up the custom logger
formatter = ColoredFormatter()

custom_logger = CustomLogger("currency_logger")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

custom_logger.addHandler(console_handler)
