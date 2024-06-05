import logging

from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, handlers=[RichHandler()])
Log = logging.getLogger("@@@ ")
