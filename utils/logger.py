
from loguru import logger as loguru_logger
import sys

def get_logger(name: str = None):
    """
    Returns a configured logger instance using loguru.
    Args:
        name (str): Optional logger name for context.
    Returns:
        loguru.logger: Configured logger
    """
    # Configure loguru to output to stdout with a standard format
    loguru_logger.remove()
    loguru_logger.add(sys.stdout, format="[{time:YYYY-MM-DD HH:mm:ss}] [{level}] [{name}] {message}", level="INFO")
    if name:
        return loguru_logger.bind(name=name)
    return loguru_logger
