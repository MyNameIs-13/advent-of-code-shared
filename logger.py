import logging
import sys
from logging import LogRecord

# --------------------------------------------------------------------
# Colors (ANSI escape codes)
# --------------------------------------------------------------------
RESET = '\033[0m'
COLORS = {
    'DEBUG': '\033[36m',   # Cyan
    'INFO': '\033[32m',    # Green
    'WARNING': '\033[33m', # Yellow
    'ERROR': '\033[31m',   # Red
    'CRITICAL': '\033[41m' # Red background
}


# --------------------------------------------------------------------
# Custom Formatter with colors + timestamps
# --------------------------------------------------------------------
class ColoredFormatter(logging.Formatter):
    def format(self, record: LogRecord):
        color = COLORS.get(record.levelname, '')
        message = super().format(record)
        return f'{color}{message}{RESET}'


# --------------------------------------------------------------------
# Global project-wide logger
# --------------------------------------------------------------------
logger = logging.getLogger('advent_of_code')
logger.setLevel(logging.INFO)  # Default; set to DEBUG to enable debug messages

# Console handler
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)  # Handler level can remain DEBUG
formatter = ColoredFormatter(
    '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.propagate = False  # Prevent double logging
